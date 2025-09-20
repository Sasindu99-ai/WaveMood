import os
import queue
import threading
import wave
from time import time
from typing import List, Optional

import joblib
import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, pyqtSlot, QRectF
from PyQt6.QtWidgets import QHBoxLayout, QFrame, QSizePolicy, QFileDialog, QVBoxLayout, QSpacerItem, QWidget
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor, QLinearGradient

import pyqtgraph as pg

from enums import TopBarMode, Model
from res import AppTheme
from vvecon.qt.contrib.styles.Button import primaryButton, secondaryButton
from vvecon.qt.contrib.styles.Label import label
from vvecon.qt.contrib.widgets import Margin, Button
from vvecon.qt.contrib.widgets.AnimatedGifLabel import AnimatedGifLabel
from vvecon.qt.contrib.widgets.Input import InputField
from vvecon.qt.contrib.widgets.QLabel import Label
from vvecon.qt.contrib.widgets.Widget import VBoxWidget
from vvecon.qt.core import View, WindowType
from vvecon.qt.enums import InputType
from vvecon.qt.logger import logger
from vvecon.qt.res import Icons
from vvecon.qt.thread import threadPool
from vvecon.qt.util import ui

try:
    from tensorflow.saved_model import load as load_model
    _tensorflow_available = True
except Exception as e:
    logger.error(f"Error importing TensorFlow/Keras: {str(e)}")
    load_model = None
    _tensorflow_available = False

__all__ = ['HomeView']


class WaveformWidget(pg.PlotWidget):
    # Signal to be emitted when waveform data is ready
    # audio_data (1d ndarray), time_points (1d ndarray), duration (float), sample_rate (int), success (bool), error_msg (str)
    waveformLoaded = pyqtSignal(object, object, float, int, bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Configure appearance
        self.setBackground('#23272F')
        self.showGrid(x=True, y=False, alpha=0.3)
        self.setMenuEnabled(False)
        self.setMouseEnabled(x=True, y=False)  # Allow x-axis zoom only
        self.getPlotItem().hideButtons()
        self.setMinimumHeight(150)

        # Set up axis labels and style
        # Fix: Use setTickFont instead of trying to get current font
        font = QFont()
        font.setPointSize(8)
        self.getAxis('bottom').setTickFont(font)
        self.getAxis('bottom').setLabel('Time (seconds)', color='#CCCCCC')
        self.getAxis('left').hide()

        # Initialize variables
        self.waveform_plot = None
        self.position_line = None
        self.audio_data = None
        self.sample_rate = None
        self.duration = 0

        # Status display for loading
        self.loading_text = pg.TextItem("Loading waveform...", color='#CCCCCC', anchor=(0.5, 0.5))
        self.loading_text.setPos(0.5, 0)
        self.addItem(self.loading_text)
        self.loading_text.hide()

        # Configure the position line (playback indicator)
        self.position_line = pg.InfiniteLine(
            pos=0,
            angle=90,
            pen=pg.mkPen(color='#E95525', width=2),
            movable=False
        )
        self.addItem(self.position_line)
        self.position_line.hide()

        # Connect signal to slot for UI updates
        self.waveformLoaded.connect(self._update_waveform_ui)

    def load_waveform(self, file_path):
        """
        Start loading the waveform - this runs in a worker thread
        """
        # NOTE: this method runs in a worker thread. Do not touch UI here.
        try:
            # Read using soundfile (works for wav/mp3/flac via libsndfile)
            data, sr = sf.read(file_path, always_2d=True)
            # Convert to mono if needed
            if data.ndim > 1 and data.shape[1] > 1:
                y = np.mean(data, axis=1)
            else:
                y = data.flatten()
            duration = len(y) / sr
            # Create x-axis time points
            time_points = np.linspace(0, duration, len(y))
            # Emit result to the main thread (slot will update UI)
            self.waveformLoaded.emit(y, time_points, duration, int(sr), True, "")
            return True
        except Exception as e:
            error_msg = f"Error loading waveform: {str(e)}"
            print(error_msg)
            self.waveformLoaded.emit(None, None, 0, 0, False, error_msg)
            return False

    @pyqtSlot(object, object, float, int, bool, str)
    def _update_waveform_ui(self, audio_data, time_points, duration, sample_rate, success, error_msg):
        """
        Update the UI with waveform data - runs in the main thread
        """
        self.loading_text.hide()

        if not success:
            # Show error message
            error_text = pg.TextItem(f"Error: {error_msg}", color='#E95525', anchor=(0.5, 0.5))
            error_text.setPos(0.5, 0)
            self.addItem(error_text)
            return

        # Store the data
        self.audio_data = audio_data
        self.sample_rate = int(sample_rate) if sample_rate else (int(len(audio_data) / duration) if duration > 0 else 0)
        self.duration = duration

        # Clear previous plot if exists
        if self.waveform_plot is not None:
            self.removeItem(self.waveform_plot)

        # Create the waveform plot
        self.waveform_plot = self.plot(
            time_points,
            audio_data,
            pen=pg.mkPen(color='#E95525', width=1.5)
        )

        # Set axis range and labels
        self.setXRange(0, duration)
        self.setYRange(-1, 1)

        # Show position line at beginning
        self.position_line.setValue(0)
        self.position_line.show()

        # Notify any listeners
        self.on_waveform_loaded()

    # helper methods to show/hide loading from main thread
    def show_loading(self):
        self.loading_text.show()

    def hide_loading(self):
        self.loading_text.hide()

    def on_waveform_loaded(self, *args, **kwargs):
        """Called when waveform is successfully loaded and rendered"""
        pass

    def update_position(self, position_sec):
        """Update the position of the playback indicator line"""
        if 0 <= position_sec <= self.duration:
            self.position_line.setValue(position_sec)

            # Auto-scroll the view to follow the position line
            view_range = self.viewRect()
            if position_sec > view_range.right() or position_sec < view_range.left():
                center = max(0, position_sec - (view_range.width() / 4))
                self.setXRange(center, center + view_range.width(), padding=0)

class VuMeterWidget(QWidget):
    """Simple horizontal jumping bars VU meter (main-thread only)."""
    def __init__(self, parent=None, num_bars=2):
        super().__init__(parent)
        self.num_bars = max(1, int(num_bars))
        self.levels = [0.0] * self.num_bars
        self.decay = 0.06
        # visual tuning
        self._corner_radius = 8
        self._padding = 10
        self.setMinimumHeight(ui.dp(56))
        self.setStyleSheet("background: transparent;")
        self.setContentsMargins(0, 0, 0, 0)

    def update_levels(self, levels):
        # Called on main thread via QTimer
        if len(levels) != self.num_bars:
            levels = levels[:self.num_bars] + [0.0] * max(0, self.num_bars - len(levels))
        for i in range(self.num_bars):
            new = float(levels[i])
            self.levels[i] = max(new, max(0.0, self.levels[i] - self.decay))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            w = self.width()
            h = self.height()

            # draw rounded card-like background with subtle border
            bg_color = QColor('#2A2F36')
            border_color = QColor('#353A42')
            painter.setPen(QPen(border_color))
            painter.setBrush(QBrush(bg_color))
            rect = self.rect().adjusted(0, 0, 0, 0)
            painter.drawRoundedRect(rect, self._corner_radius, self._corner_radius)

            # inner drawing area
            inner_x = self._padding
            inner_w = max(8, w - 2 * self._padding)
            inner_y = self._padding
            inner_h = max(8, h - 2 * self._padding)

            # spacing between stacked horizontal bars
            spacing = max(6, int(inner_h * 0.12))
            total_spacing = spacing * (self.num_bars + 1)
            bar_h = max(6, int((inner_h - total_spacing) / max(1, self.num_bars)))

            for i, lvl in enumerate(self.levels):
                level = float(min(1.0, max(0.0, lvl)))
                y = inner_y + spacing + i * (bar_h + spacing)
                length = int(round(inner_w * level))

                # color by thresholds and soft gradient
                if level < 0.6:
                    start_col = QColor(98, 200, 120)
                    end_col = QColor(60, 180, 100)
                elif level < 0.85:
                    start_col = QColor(255, 214, 102)
                    end_col = QColor(255, 190, 40)
                else:
                    start_col = QColor(250, 120, 120)
                    end_col = QColor(220, 60, 60)

                # draw filled portion with subtle gradient
                if length > 0:
                    grad_rect = QRectF(inner_x, y, length, bar_h)
                    grad = QLinearGradient(grad_rect.topLeft(), grad_rect.topRight())
                    grad.setColorAt(0.0, start_col)
                    grad.setColorAt(1.0, end_col)
                    painter.setBrush(QBrush(grad))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawRoundedRect(grad_rect, bar_h / 2, bar_h / 2)

                # draw track for remaining area
                track_rect = QRectF(inner_x + length, y, max(0, inner_w - length), bar_h)
                painter.setBrush(QBrush(QColor(80, 86, 92, 140)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(track_rect, bar_h / 2, bar_h / 2)
        finally:
            painter.end()

class HomeView(View):
    _sampleRate = 22050
    _frameRate = 44100
    modelButtons: List[Button] = []

    def __init__(self, parent: Optional[WindowType] = None):
        super(HomeView, self).__init__(parent, 'Home')
        self.setObjectName('HomeView')

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.layout.setContentsMargins(Margin(20))
        self.layout.setSpacing(ui.dp(20))
        self.setSizePolicy(ui.sizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        ))

        # --- Config section with improved visual design ---
        self.config = VBoxWidget(self, spacing=ui.dp(16))
        self.config.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.config.setFixedWidth(ui.dp(220))

        # Create a styled frame for the model selection
        self.modelFrame = QFrame(self.config)
        self.modelFrame.setStyleSheet("""
            QFrame {
                background: #23272F;
                border-radius: 18px;
                border: 1px solid #353A42;
            }
        """)
        self.modelLayout = QVBoxLayout(self.modelFrame)
        self.modelLayout.setContentsMargins(ui.dp(16), ui.dp(16), ui.dp(16), ui.dp(16))
        self.modelLayout.setSpacing(ui.dp(12))

        # Model section header
        self.modelLabel = Label('Select Model', parent=self.modelFrame)
        self.modelLabel.setStyleSheet(label.update(
            backgroundColor='transparent', color='#FFFFFF', fontSize=16, fontWeight='600'
        ).qss)
        self.modelLayout.addWidget(self.modelLabel)

        # Style model buttons better
        self.modelBtnGroup = QFrame(self.modelFrame)
        self.modelBtnGroup.setStyleSheet("background: transparent; border: none;")
        self.modelBtnLayout = QVBoxLayout(self.modelBtnGroup)
        self.modelBtnLayout.setContentsMargins(0, 0, 0, 0)
        self.modelBtnLayout.setSpacing(ui.dp(10))

        # map models to buttons so we can treat them like radio buttons
        self._modelButtonMap = {}
        # default active model
        self._activeModel = Model.MLP
        for model in Model:
            # create checkable button
            btn = Button(
                model.value,
                icon=ui.icon(AppTheme.images.getImage(model.value.lower())),
                style=Qt.ToolButtonStyle.ToolButtonTextBesideIcon,
                iconSize=ui.size(30, 30)
            )
            btn.setFixedHeight(ui.dp(46))
            btn.setCheckable(True)
            # initial checked and style
            is_active = (model == self._activeModel)
            btn.setChecked(is_active)
            if is_active:
                btn.setStyleSheet(primaryButton.update(
                    backgroundColor='#E95525',
                    color='#FFFFFF',
                    fontWeight='600',
                    radius=10,
                    hoverColor='#C15532',
                ).qss)
            else:
                btn.setStyleSheet(secondaryButton.update(
                    backgroundColor='#353A42',
                    color='#CCCCCC',
                    border='1px solid #454A52',
                    fontWeight='500',
                    radius=10,
                    hoverColor='#3A3F47',
                ).qss)

            # Disable MLP button if TensorFlow is not available
            if model == Model.MLP and not _tensorflow_available:
                btn.setEnabled(False)
                btn.setToolTip("MLP model unavailable: TensorFlow not loaded")
                if is_active:
                    self._activeModel = Model.KNN  # fallback to KNN

            # connect click to model selector (ignore passed checked arg)
            btn.onClick(lambda checked, m=model: self._onModelSelected(m))

            self.modelButtons.append(btn)
            self._modelButtonMap[model] = btn
            self.modelBtnLayout.addWidget(btn)

        self.modelLayout.addWidget(self.modelBtnGroup)
        self.config.addWidget(self.modelFrame)

        # Create styled frame for audio settings
        self.settingsFrame = QFrame(self.config)
        self.settingsFrame.setStyleSheet("""
            QFrame {
                background: #23272F;
                border-radius: 18px;
            }
        """)
        self.settingsLayout = QVBoxLayout(self.settingsFrame)
        self.settingsLayout.setContentsMargins(ui.dp(16), ui.dp(16), ui.dp(16), ui.dp(16))
        self.settingsLayout.setSpacing(ui.dp(14))

        # Settings section header
        self.settingsLabel = Label('Audio Settings', parent=self.settingsFrame)
        self.settingsLabel.setStyleSheet(label.update(
            backgroundColor='transparent', color='#FFFFFF', fontSize=16, fontWeight='600', border='none'
        ).qss)
        self.settingsLayout.addWidget(self.settingsLabel)

        # Styled input fields with icons
        self.sampleRateInput = InputField(
            name='Sample Rate',
            placeholder='Sample Rate',
            parent=self.settingsFrame,
            inType=InputType.NUMBER,
            minVal=0,
            icon=Icons.Rounded.equalizer
        )
        self.sampleRateInput.setValue(self._sampleRate)

        self.frameRateInput = InputField(
            name='Frame Rate',
            placeholder='Frame Rate',
            parent=self.settingsFrame,
            inType=InputType.NUMBER,
            minVal=0,
            icon=Icons.Rounded.speed
        )
        self.frameRateInput.setValue(self._frameRate)

        self.settingsLayout.addWidget(self.sampleRateInput)
        self.settingsLayout.addWidget(self.frameRateInput)

        self.config.addSpacing(ui.dp(16))
        self.config.addWidget(self.settingsFrame)
        self.config.addStretch(1)

        self.separator1 = QFrame(self)
        self.separator1.setFrameShape(QFrame.Shape.VLine)
        self.separator1.setFrameShadow(QFrame.Shadow.Sunken)
        self.separator1.setLineWidth(1)
        self.separator1.setMidLineWidth(0)

        self.body = VBoxWidget(self)
        self.body.setSizePolicy(ui.sizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        ))
        self.body.setContentsMargins(Margin(0))  # Remove side margins for full width
        self.body.setMinimumWidth(400)

        # --- Top section for file selection and recording ---
        # Top section frame: always at top, max width, fixed height
        self.topSectionFrame = QFrame(self.body)
        self.topSectionFrame.setStyleSheet("""
            QFrame {
                background: #23272F;
                border-radius: 18px;
                border: 1px solid #353A42;
            }
        """)
        self.topSectionFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.topSectionFrame.setMaximumWidth(9999)
        self.topSectionFrame.setMinimumHeight(ui.dp(110))
        self.topSectionLayout = QVBoxLayout(self.topSectionFrame)
        self.topSectionLayout.setContentsMargins(ui.dp(24), ui.dp(18), ui.dp(24), ui.dp(18))
        self.topSectionLayout.setSpacing(ui.dp(18))

        # Selected file field
        self.selectedFileLabel = Label('No file selected', parent=self.topSectionFrame)
        self.selectedFileLabel.setStyleSheet(label.update(
            backgroundColor='#23272F', color='#CCCCCC', fontSize=14, border='none', radius=8
        ).qss)
        self.selectedFileLabel.setFixedHeight(ui.dp(40))  # Increase height to accommodate multiple lines
        self.selectedFileLabel.setWordWrap(True)  # Enable text wrapping
        self.selectedFileLabel.setContentsMargins(ui.dp(8), ui.dp(4), ui.dp(8), ui.dp(4))

        # Select file button with icon
        self.selectFileBtn = Button(
            'Select Audio File',
            icon=Icons.Rounded.folder_open,
            iconSize=ui.size(22, 22),
            styleSheet=secondaryButton.update(
                backgroundColor='#353A42', color='#E95525', fontWeight='600', radius=8
            ).qss
        )
        self.selectFileBtn.onClick(self._onSelectFile)

        fileRow = QHBoxLayout()
        fileRow.setSpacing(ui.dp(12))
        fileRow.addWidget(self.selectedFileLabel, stretch=1)
        fileRow.addWidget(self.selectFileBtn)
        self.topSectionLayout.addLayout(fileRow)

        self.topSectionLayout.addSpacing(ui.dp(10))

        # Recording controls row
        self.recordingLayout = QHBoxLayout()
        self.recordingLayout.setSpacing(ui.dp(14))

        # Record button with mic icon
        self.recordBtn = Button(
            'Record',
            icon=Icons.Rounded.mic,
            iconSize=ui.size(22, 22),
            styleSheet=primaryButton.update(
                backgroundColor='#E95525', color='white', fontWeight='600', radius=8
            ).qss
        )
        self.stopBtn = Button(
            'Stop',
            icon=Icons.Rounded.stop_circle,
            iconSize=ui.size(22, 22),
            styleSheet=secondaryButton.update(
                backgroundColor='#353A42', color='#E95525', fontWeight='600', radius=8
            ).qss
        )
        self.stopBtn.setEnabled(False)
        self.recordBtn.onClick(self._onStartRecording)
        self.stopBtn.onClick(self._onStopRecording)

        # Animated GIF for recording indicator
        self.recordingGif = AnimatedGifLabel(AppTheme.images.recording, parent=self.topSectionFrame)
        self.recordingGif.setFixedSize(ui.dp(32), ui.dp(32))  # Increased size
        self.recordingGif.hide()

        # Blinking/glowing red circle (bulb effect)
        self.redCircle = Label('', parent=self.topSectionFrame)
        self.redCircle.setFixedSize(ui.dp(18), ui.dp(18))
        self.redCircle.setStyleSheet("""
            QLabel {
                border-radius: 9px;
                background: #B00020;
                box-shadow: 0 0 16px #B00020;
                opacity: 1;
                transition: opacity 0.2s;
            }
        """)
        self.redCircle.hide()
        self._blinkTimer = QTimer(self)
        self._blinkTimer.timeout.connect(self._toggleRedCircleGlow)
        self._redGlow = True

        # Recording status text
        self.recordingStatus = Label('', parent=self.topSectionFrame)
        self.recordingStatus.setStyleSheet(label.update(
            backgroundColor='transparent', color='#E95525', fontSize=14, fontWeight='600'
        ).qss)

        self.recordingLayout.addWidget(self.recordBtn)
        self.recordingLayout.addWidget(self.stopBtn)
        self.recordingLayout.addSpacing(ui.dp(10))
        self.recordingLayout.addWidget(self.recordingGif)
        self.recordingLayout.addWidget(self.recordingStatus, stretch=1)
        self.topSectionLayout.addLayout(self.recordingLayout)

        self.body.addWidget(self.topSectionFrame)
        self.body.addSpacing(ui.dp(16))  # Reduced spacing

        # --- Audio Controls Section ---
        self.audioControlFrame = QFrame(self.body)
        self.audioControlFrame.setStyleSheet("""
            QFrame {
                background: #23272F;
                border-radius: 18px;
                border: 1px solid #353A42;
            }
        """)
        self.audioControlFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.audioControlFrame.setMaximumWidth(9999)
        self.audioControlLayout = QHBoxLayout(self.audioControlFrame)
        self.audioControlLayout.setContentsMargins(ui.dp(24), ui.dp(16), ui.dp(24), ui.dp(16))
        self.audioControlLayout.setSpacing(ui.dp(14))

        # Play/Pause Button
        self.playPauseBtn = Button(
            'Play',
            icon=Icons.Filled.Rounded.play_arrow.update(color='#1e6e0f'),
            iconSize=ui.size(22, 22),
            styleSheet=secondaryButton.update(
                backgroundColor='#353A42', color='#E95525', fontWeight='600', radius=8
            ).qss
        )
        self.playPauseBtn.onClick(self._togglePlayPause)

        # Stop Button
        self.audioStopBtn = Button(
            'Stop',
            icon=Icons.Filled.Rounded.stop.update(color='#E95525'),
            iconSize=ui.size(22, 22),
            styleSheet=secondaryButton.update(
                backgroundColor='#353A42', color='#E95525', fontWeight='600', radius=8
            ).qss
        )
        self.audioStopBtn.onClick(self._stopPlayback)
        self.audioStopBtn.setEnabled(False)  # Disabled initially

        # Status label
        self.playbackStatus = Label('', parent=self.audioControlFrame)
        self.playbackStatus.setStyleSheet(label.update(
            backgroundColor='transparent', color='#CCCCCC', fontSize=14, fontWeight='500'
        ).qss)

        # Add spacer to push analyze button to the right
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Analyze Button (right-aligned)
        self.analyzeBtn = Button(
            'Analyze',
            icon=Icons.Rounded.analytics,
            iconSize=ui.size(22, 22),
            styleSheet=primaryButton.update(
                backgroundColor='#E95525', color='balck', fontWeight='600', radius=8
            ).qss,
            style=Qt.ToolButtonStyle.ToolButtonTextBesideIcon, spaceBetween=2
        )
        self.analyzeBtn.onClick(self._analyzeAudio)

        # Add widgets to layout
        self.audioControlLayout.addWidget(self.playPauseBtn)
        self.audioControlLayout.addWidget(self.audioStopBtn)
        self.audioControlLayout.addWidget(self.playbackStatus)
        self.audioControlLayout.addItem(spacerItem)
        self.audioControlLayout.addWidget(self.analyzeBtn)

        self.body.addWidget(self.audioControlFrame)
        self.body.addSpacing(ui.dp(16))

        # --- Waveform Display Section ---
        self.waveformFrame = QFrame(self.body)
        self.waveformFrame.setStyleSheet("""
            QFrame {
                background: #23272F;
                border-radius: 18px;
                border: 1px solid #353A42;
            }
        """)
        self.waveformFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.waveformFrame.setMaximumWidth(9999)
        self.waveformLayout = QVBoxLayout(self.waveformFrame)
        self.waveformLayout.setContentsMargins(ui.dp(14), ui.dp(14), ui.dp(14), ui.dp(14))
        self.waveformLayout.setSpacing(ui.dp(8))

        # Waveform title
        self.waveformTitle = Label('Audio Waveform', parent=self.waveformFrame)
        self.waveformTitle.setStyleSheet(label.update(
            backgroundColor='transparent', color='#FFFFFF', fontSize=14, fontWeight='600'
        ).qss)

        # Add waveform widget
        self.waveformWidget = WaveformWidget(parent=self.waveformFrame)

        self.waveformLayout.addWidget(self.waveformTitle)
        self.waveformLayout.addWidget(self.waveformWidget)

        self.body.addWidget(self.waveformFrame)
        self.body.addSpacing(ui.dp(16))

        # --- VU meter (below waveform) ---
        self.vuFrame = QFrame(self.body)
        # card style consistent with other sections
        self.vuFrame.setStyleSheet("""
            QFrame {
                background: #23272F;
                border-radius: 12px;
                border: 1px solid #353A42;
            }
        """)
        self.vuFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vuFrame.setMinimumHeight(ui.dp(72))
        # inner horizontal layout: label (left) + widget (stretch)
        self.vuLayout = QHBoxLayout(self.vuFrame)
        self.vuLayout.setContentsMargins(ui.dp(12), ui.dp(10), ui.dp(12), ui.dp(10))
        self.vuLayout.setSpacing(ui.dp(12))

        # small title/label
        self.vuLabel = Label('Volume', parent=self.vuFrame)
        self.vuLabel.setStyleSheet(label.update(
            backgroundColor='transparent', color='#CCCCCC', fontSize=13, fontWeight='600'
        ).qss)
        self.vuLabel.setFixedWidth(ui.dp(80))

        # show only two horizontal jumping bars
        self.vuWidget = VuMeterWidget(parent=self.vuFrame, num_bars=2)
        self.vuWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.vuLayout.addWidget(self.vuLabel)
        self.vuLayout.addWidget(self.vuWidget, stretch=1)
        self.body.addWidget(self.vuFrame)
        self.body.addSpacing(ui.dp(20))
        # keep main stretch below
        self.body.addStretch()

        self.separator2 = QFrame(self)
        self.separator2.setFrameShape(QFrame.Shape.VLine)
        self.separator2.setFrameShadow(QFrame.Shadow.Sunken)
        self.separator2.setLineWidth(1)
        self.separator2.setMidLineWidth(0)

        # Analysis results section (placeholder)

        self.layout.addWidget(self.config)
        self.layout.addWidget(self.separator1)
        self.layout.addWidget(self.body, stretch=1)
        self.layout.addWidget(self.separator2)
        self.setLayout(self.layout)

        # Recording state
        self._recording = False
        self._audioQueue = queue.Queue()
        self._recordingThread = None
        self._audioData = None

        # lock to protect _audioData access between threads
        self._record_lock = threading.Lock()

        # recordings directory (AppData\WaveMood\recordings on Windows, fallback to user home)
        self._recordingsDir = os.path.join(
            os.getenv('APPDATA') or os.path.expanduser('~'),
            'WaveMood',
            'recordings'
        )
        try:
            os.makedirs(self._recordingsDir, exist_ok=True)
        except Exception as _e:
            # best-effort: if creation fails, fall back to current working directory
            self._recordingsDir = os.path.join(os.path.expanduser('~'), 'WaveMood', 'recordings')
            try:
                os.makedirs(self._recordingsDir, exist_ok=True)
            except Exception:
                # if this also fails, leave value and let _saveRecording handle errors
                pass
        # ensure InputStream uses consistent dtype

        # --- Playback state (initialize to avoid AttributeError) ---
        self._isPlaying = False
        self._playbackThread = None
        self._playbackStream = None
        self._playbackPosition = 0.0
        self._playbackUpdateTimer = QTimer(self)
        self._playbackUpdateTimer.setInterval(50)  # 50ms updates
        self._playbackUpdateTimer.timeout.connect(self._updatePlaybackPosition)

        # playback frame index and lock so we can resume/track progress safely
        self._playbackFrameIndex = 0
        self._playbackFrameLock = threading.Lock()
        # track current audio file path
        self._currentAudioFile = None

        # VU meter state: thread-safe latest level (0..1)
        self._vu_lock = threading.Lock()
        self._vu_level = 0.0
        self._vuTimer = QTimer(self)
        self._vuTimer.setInterval(50)  # 20 FPS
        self._vuTimer.timeout.connect(self._updateVuMeter)

    # --- File selection ---
    def _onSelectFile(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", "", "Audio Files (*.wav *.mp3 *.flac)"
        )
        if filePath:
            self.selectedFileLabel.setText(filePath)
            self.playbackStatus.setText("Loading waveform...")

            # Show loading indicator (UI thread) then start background job
            self.waveformWidget.show_loading()
            threadPool.start(
                self.waveformWidget.load_waveform,
                filePath,
                callback=lambda success: self._onWaveformLoaded(success, filePath)
            )
        else:
            self.selectedFileLabel.setText('No file selected')

    def _onWaveformLoaded(self, success, file_path):
        """Callback when waveform loading is complete"""
        if success:
            self.playbackStatus.setText(f"Ready to play: {os.path.basename(file_path)}")
            # update current audio file so playback uses latest selected/recorded file
            self._currentAudioFile = file_path
        else:
            self.playbackStatus.setText("Error loading waveform")

    # --- Recording logic ---
    def _onStartRecording(self):
        self._recording = True
        # clear queue and buffer safely
        with self._record_lock:
            # clear any previous data
            self._audioData = []
        # clear underlying queue if needed
        try:
            while True:
                self._audioQueue.get_nowait()
        except queue.Empty:
            pass
        self.recordBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)
        self.recordingStatus.setText('Recording...')
        self.recordingGif.show()
        self.recordingGif.start()
        self._recordingThread = threading.Thread(target=self._recordAudio, daemon=True)
        self._recordingThread.start()

    def _onStopRecording(self):
        # signal recording thread to stop
        self._recording = False
        self.recordBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)
        self.recordingStatus.setText('Recording stopped')
        self.recordingGif.stop()
        self.recordingGif.hide()

        # wait briefly for recording thread to consume remaining frames
        if self._recordingThread and self._recordingThread.is_alive():
            # join with timeout to avoid blocking UI indefinitely
            self._recordingThread.join(timeout=3.0)
            # after join attempt, make a final pass to drain queue into buffer
            try:
                while True:
                    chunk = self._audioQueue.get_nowait()
                    with self._record_lock:
                        if self._audioData is None:
                            self._audioData = []
                        self._audioData.append(chunk)
            except queue.Empty:
                pass
        # next: save (runs on main thread)
        self._saveRecording()
        # clear thread reference
        self._recordingThread = None

    def _toggleRedCircleGlow(self):
        # Animate glow by changing box-shadow intensity, not opacity
        if self._redGlow:
            self.redCircle.setStyleSheet("""
                QLabel {
                    border-radius: 9px;
                    background: #B00020;
                    box-shadow: 0 0 32px #B00020;
                    opacity: 1;
                    transition: box-shadow 0.2s;
                }
            """)
        else:
            self.redCircle.setStyleSheet("""
                QLabel {
                    border-radius: 9px;
                    background: #B00020;
                    box-shadow: 0 0 8px #B00020;
                    opacity: 1;
                    transition: box-shadow 0.2s;
                }
            """)
        self._redGlow = not self._redGlow

    def _recordAudio(self):
        def callback(indata, frames, time, status):
            # protect callback from exceptions escaping into sounddevice internals
            if status:
                # non-fatal status information; keep as debug if needed
                # print("Record status:", status)
                pass
            try:
                if self._recording:
                    # copy to own memory
                    self._audioQueue.put(indata.copy(), block=False)
            except queue.Full:
                # queue full: drop frame
                pass
            except Exception:
                # avoid raising in callback
                pass
        # run input stream in this thread. use float32 dtype for predictable behaviour.
        try:
            with sd.InputStream(samplerate=self._sampleRate, channels=1, dtype='float32', callback=callback):
                while self._recording:
                    try:
                        data = self._audioQueue.get(timeout=0.1)
                        with self._record_lock:
                            if self._audioData is None:
                                self._audioData = []
                            self._audioData.append(data)
                    except queue.Empty:
                        continue
                # after stop requested, drain any remaining queued frames
                try:
                    while True:
                        data = self._audioQueue.get_nowait()
                        with self._record_lock:
                            if self._audioData is None:
                                self._audioData = []
                            self._audioData.append(data)
                except queue.Empty:
                    pass
        except Exception as e:
            # record errors should not crash the app; update status on main thread if possible
            print("InputStream error:", e)

    def _saveRecording(self):
        # Collect and write recorded buffers safely
        with self._record_lock:
            if not self._audioData:
                return
            try:
                audio = np.concatenate(self._audioData, axis=0)
            except Exception:
                # fallback: try to stack as 1-D flatten
                audio = np.asarray(self._audioData).reshape(-1)

        # Ensure mono 1-D float array
        audio = np.asarray(audio, dtype=np.float32).flatten()
        # Clip to valid range and convert to int16
        audio = np.clip(audio, -1.0, 1.0)
        int16_audio = (audio * 32767.0).astype(np.int16)

        filename = f"recording_{int(threading.get_native_id())}_{int(time())}.wav"
        filepath = os.path.join(self._recordingsDir, filename)
        try:
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self._sampleRate)
                wf.writeframes(int16_audio.tobytes())
        except Exception as e:
            print("Error saving recording:", e)
            self.recordingStatus.setText('Error saving recording')
            return

        # update UI
        self.selectedFileLabel.setText(filepath)
        self.recordingStatus.setText(f"Saved: {os.path.basename(filepath)}")

        # Load the waveform for the newly recorded audio (start loading in background)
        self.playbackStatus.setText("Loading waveform...")
        self.waveformWidget.show_loading()
        threadPool.start(
            self.waveformWidget.load_waveform,
            filepath,
            callback=lambda success: self._onWaveformLoaded(success, filepath)
        )

    # --- Audio Playback Methods ---
    def _togglePlayPause(self):
        if not self.selectedFileLabel.text() or self.selectedFileLabel.text() == 'No file selected':
            self.playbackStatus.setText('Please select an audio file first')
            return

        if self._isPlaying:
            self._pausePlayback()
        else:
            self._startPlayback()

    def _startPlayback(self):
        self._isPlaying = True
        self.playPauseBtn.setText('Pause')
        self.playPauseBtn.setIcon(Icons.Filled.Rounded.pause.update(color='#0659ad'))
        self.audioStopBtn.setEnabled(True)

        # Get file path from selectedFileLabel (prefer _currentAudioFile)
        file_path = self._currentAudioFile or self.selectedFileLabel.text()
        if not file_path or file_path == 'No file selected':
            self.playbackStatus.setText('Please select an audio file first')
            self._isPlaying = False
            self.playPauseBtn.setText('Play')
            return

        # Start playback in a separate thread, resume from stored frame index
        start_frame = 0
        with self._playbackFrameLock:
            start_frame = int(self._playbackFrameIndex or 0)
        self._playbackThread = threading.Thread(target=self._playAudio, args=(file_path, start_frame), daemon=True)
        self._playbackThread.start()

        # Start updating position indicator
        self._playbackUpdateTimer.start()

        # start VU UI timer (main thread) so bars update while playing
        try:
            self._vuTimer.start()
        except Exception:
            pass

        self.playbackStatus.setText('Playing...')

    def _pausePlayback(self):
        # set playing flag false so callback will stop advancing
        self._isPlaying = False
        self.playPauseBtn.setText('Play')
        self.playPauseBtn.setIcon(Icons.Filled.Rounded.play_arrow.update(color='#1e6e0f'))
        self.playbackStatus.setText('Paused')

        # Stop updating position indicator
        self._playbackUpdateTimer.stop()

        # stop VU updates and clear display
        try:
            self._vuTimer.stop()
            with self._vu_lock:
                self._vu_level = 0.0
            if hasattr(self, 'vuWidget') and self.vuWidget:
                self.vuWidget.update_levels([0.0] * self.vuWidget.num_bars)
        except Exception:
            pass

        # If there's an active stream, stop+close it and join the thread.
        # We keep _playbackFrameIndex so resume will continue from this point.
        if self._playbackStream:
            try:
                self._playbackStream.stop()
            except Exception:
                pass
            try:
                self._playbackStream.close()
            except Exception:
                pass
            self._playbackStream = None

        # join the playback thread (non-blocking UI: short timeout)
        if self._playbackThread and self._playbackThread.is_alive():
            self._playbackThread.join(timeout=0.5)
            if self._playbackThread.is_alive():
                # leave it; it should exit soon
                pass
        self._playbackThread = None

    def _stopPlayback(self):
        self._isPlaying = False
        self.playPauseBtn.setText('Play')
        self.playPauseBtn.setIcon(Icons.Filled.Rounded.play_arrow.update(color='#1e6e0f'))
        self.audioStopBtn.setEnabled(False)
        self.playbackStatus.setText('Stopped')

        # Reset playback position and stop updating
        self._playbackPosition = 0
        self._playbackUpdateTimer.stop()
        # reset waveform cursor to start
        self.waveformWidget.update_position(0)

        # stop and reset VU meter
        try:
            self._vuTimer.stop()
            with self._vu_lock:
                self._vu_level = 0.0
            if hasattr(self, 'vuWidget') and self.vuWidget:
                self.vuWidget.update_levels([0.0] * self.vuWidget.num_bars)
        except Exception:
            pass

        # Stop and close the stream if it exists and reset frame index
        if self._playbackStream:
            try:
                self._playbackStream.stop()
            except Exception:
                pass
            try:
                self._playbackStream.close()
            except Exception:
                pass
            self._playbackStream = None

        with self._playbackFrameLock:
            # reset frame index so next play starts from zero
            self._playbackFrameIndex = 0

        # join the playback thread
        if self._playbackThread and self._playbackThread.is_alive():
            self._playbackThread.join(timeout=0.5)
            self._playbackThread = None

    def _playAudio(self, file_path, start_frame: int = 0):
        try:
            # Read audio file
            import soundfile as sf
            data, samplerate = sf.read(file_path, always_2d=True)
            # store current audio file
            self._currentAudioFile = file_path

            # Reset playback position
            # set initial frame index from argument
            with self._playbackFrameLock:
                frame_index = int(start_frame or 0)
                self._playbackFrameIndex = frame_index
            self._playbackPosition = frame_index / samplerate if samplerate else 0.0

            # Define callback function
            # Ensure data is 2D (frames, channels)
            if data.ndim == 1:
                data = np.expand_dims(data, axis=1)

            def callback(outdata, frames, time, status):
                nonlocal frame_index
                if not self._isPlaying:
                    outdata.fill(0)
                    return

                remaining = data.shape[0] - frame_index
                if remaining <= 0:
                    outdata.fill(0)
                    # reached end - schedule main-thread stop
                    QTimer.singleShot(0, self._autoStopPlayback)
                    return

                to_copy = min(frames, remaining)
                current_data = data[frame_index:frame_index + to_copy]
                outdata[:to_copy] = current_data
                if to_copy < frames:
                    outdata[to_copy:].fill(0)

                # compute a simple RMS-based level for VU (thread-safe write)
                try:
                    flat = current_data.flatten().astype(np.float32)
                    if flat.size:
                        rms = np.sqrt(np.mean(flat * flat))
                        # map rms -> normalized 0..1
                        # use a simple linear gain mapping to be robust for various levels
                        norm = max(0.0, min(1.0, rms * 20.0))
                    else:
                        norm = 0.0
                except Exception:
                    norm = 0.0
                with self._vu_lock:
                    self._vu_level = float(norm)

                # update shared frame index and playback position
                frame_index += to_copy
                with self._playbackFrameLock:
                    self._playbackFrameIndex = frame_index
                # update approximate playback position (seconds)
                self._playbackPosition = frame_index / samplerate if samplerate else 0.0

            # Start output stream
            self._playbackStream = sd.OutputStream(
                samplerate=samplerate,
                channels=data.shape[1],
                dtype='float32',
                callback=callback
            )
            # start stream and set playing flag (in case resumed)
            self._playbackStream.start()

            # VU timer is managed from main thread (_startPlayback/_pause/_stop)

            # keep running while stream is active and playing flag may be toggled by pause/stop
            # sounddevice handles the callback; return when stream is stopped/closed
            while self._playbackStream and self._playbackStream.active:
                # if not playing, sleep briefly; callback outputs silence
                if not self._isPlaying:
                    sd.sleep(50)
                else:
                    sd.sleep(20)
            # ensure stream closed
            try:
                if self._playbackStream:
                    self._playbackStream.stop()
            except Exception:
                pass
            try:
                if self._playbackStream:
                    self._playbackStream.close()
            except Exception:
                pass
            self._playbackStream = None

            # VU timer will be stopped by main-thread stop/pause handlers

        except Exception as e:
            # Ensure UI updated on error
            QTimer.singleShot(0, lambda: self.playbackStatus.setText(f"Error playing file: {str(e)}"))
            self._isPlaying = False
            QTimer.singleShot(0, lambda: self.playPauseBtn.setText('Play'))
            QTimer.singleShot(0, lambda: self.playPauseBtn.setIcon(Icons.Filled.Rounded.play_arrow.update(color='#1e6e0f')))
            QTimer.singleShot(0, lambda: self.audioStopBtn.setEnabled(False))
            self._playbackUpdateTimer.stop()
            # ensure VU timer stopped on error
            QTimer.singleShot(0, lambda: self._vuTimer.stop())

    def _autoStopPlayback(self):
        """Called when playback reaches the end of the file"""
        # Stop playing and ensure stream closed
        self._isPlaying = False
        self.playPauseBtn.setText('Play')
        self.playPauseBtn.setIcon(Icons.Filled.Rounded.play_arrow.update(color='#1e6e0f'))
        self.audioStopBtn.setEnabled(False)
        self.playbackStatus.setText('Playback completed')
        self._playbackUpdateTimer.stop()

        # close and clear stream if exists and reset frame index
        if self._playbackStream:
            try:
                self._playbackStream.stop()
            except Exception:
                pass
            try:
                self._playbackStream.close()
            except Exception:
                pass
            self._playbackStream = None

        with self._playbackFrameLock:
            # reset frame index so next play starts from zero
            self._playbackFrameIndex = 0

        # join the playback thread
        if self._playbackThread and self._playbackThread.is_alive():
            self._playbackThread.join(timeout=0.5)
            self._playbackThread = None

        # fully reset playback to initial state so UI and cursor return to start
        with self._playbackFrameLock:
            self._playbackFrameIndex = 0
        self._playbackPosition = 0
        # move waveform cursor to start
        self.waveformWidget.update_position(0)
        # ensure VU cleared and timer stopped
        try:
            self._vuTimer.stop()
            with self._vu_lock:
                self._vu_level = 0.0
            if hasattr(self, 'vuWidget') and self.vuWidget:
                self.vuWidget.update_levels([0.0] * self.vuWidget.num_bars)
        except Exception:
            pass
        # ensure playback thread reference cleared
        if self._playbackThread and self._playbackThread.is_alive():
            try:
                self._playbackThread.join(timeout=0.5)
            except Exception:
                pass
        self._playbackThread = None

    # --- Analysis / model helpers (new) ---
    def _ensure_models_loaded(self):
        """Lazy-load models/scalers/encoders in background thread. Returns (ok, err_msg)."""
        if getattr(self, '_models_initialized', False):
            return True, ''
        try:
            base = os.getcwd()  # expect model files in project root or adjust as needed
            # load mlp model if available and keras is importable
            if load_model and _tensorflow_available and not hasattr(self, '_mlp_model'):
                mlp_path = os.path.join(base, 'emotiondetector_mlp_model.h5')
                if os.path.exists(mlp_path):
                    self._mlp_model = load_model(mlp_path)
            # scalers / encoders
            scaler_path = os.path.join(base, 'emotion_scaler.pkl')
            le_path = os.path.join(base, 'emotion_labelencoder.pkl')
            knn_path = os.path.join(base, 'knn_emotion_model.pkl')
            if os.path.exists(scaler_path) and not hasattr(self, '_scaler_mlp'):
                self._scaler_mlp = joblib.load(scaler_path)
            if os.path.exists(le_path) and not hasattr(self, '_le_encoder'):
                self._le_encoder = joblib.load(le_path)
            if os.path.exists(knn_path) and not hasattr(self, '_knn_model'):
                self._knn_model = joblib.load(knn_path)
            self._models_initialized = True
            return True, ''
        except Exception as e:
            return False, str(e)

    def _estimate_f0_autocorr(self, frame, sr, fmin=50, fmax=800):
        """Estimate f0 for a short frame using autocorrelation. Returns f0 in Hz or 0.0."""
        try:
            # window and zero-mean
            x = frame - np.mean(frame)
            if x.size < 3:
                return 0.0
            corr = np.correlate(x, x, mode='full')
            corr = corr[corr.size // 2:]
            # ignore zero-lag
            corr[0] = 0.0
            # define lag range
            min_lag = int(sr / fmax) if fmax > 0 else 1
            max_lag = int(sr / fmin) if fmin > 0 else len(corr) - 1
            max_lag = min(max_lag, len(corr) - 1)
            if max_lag <= min_lag:
                return 0.0
            peak_region = corr[min_lag:max_lag + 1]
            if peak_region.size == 0:
                return 0.0
            peak = np.argmax(peak_region) + min_lag
            if corr[peak] <= 0:
                return 0.0
            f0 = float(sr) / float(peak) if peak > 0 else 0.0
            return float(f0)
        except Exception:
            return 0.0

    def _extract_window_features(self, sig, sr):
        """
        Given a 1-D signal for one window, split into small frames and compute arrays:
        f0_contour, energy_contour — these mirror the original ML_feed expectations.
        """
        try:
            frame_len = int(sr * 0.06)  # 60ms
            hop = int(frame_len // 2)
            if frame_len < 16:
                frame_len = 256
                hop = 128
            frames = []
            for start in range(0, max(1, len(sig) - frame_len + 1), hop):
                frames.append(sig[start:start + frame_len])
            if not frames:
                frames = [sig]
            f0s = []
            energies = []
            for fr in frames:
                # energy (RMS)
                frf = np.asarray(fr, dtype=np.float32)
                if frf.size == 0:
                    energies.append(0.0)
                    f0s.append(0.0)
                    continue
                rms = float(np.sqrt(np.mean(frf * frf)))
                energies.append(rms)
                # estimate f0 via autocorr
                f0 = self._estimate_f0_autocorr(frf, sr)
                f0s.append(f0)
            return np.array(f0s, dtype=np.float32), np.array(energies, dtype=np.float32)
        except Exception:
            return np.array([], dtype=np.float32), np.array([], dtype=np.float32)

    def _run_analysis(self, file_path, model_choice: str = 'mlp'):
        """
        Worker function: segment file into overlapping windows, extract features per window,
        predict per-window emotion and probabilities, aggregate results.
        Returns a dict result.
        """
        result = {'ok': False, 'error': '', 'timeline': [], 'summary': {}}
        try:
            ok, err = self._ensure_models_loaded()
            if not ok:
                result['error'] = f"Model load error: {err}"
                return result

            # read audio using soundfile
            data, sr = sf.read(file_path, always_2d=True)
            # mono
            if data.ndim > 1 and data.shape[1] > 1:
                sig = np.mean(data, axis=1)
            else:
                sig = data.flatten()
            total_len = len(sig)
            total_sec = total_len / float(sr) if sr else 0.0
            # sliding windows
            win_sec = 1.0
            hop_sec = 0.5
            win = int(win_sec * sr)
            hop = int(hop_sec * sr)
            if win <= 0:
                win = total_len
                hop = win
            idx = 0
            window_predictions = []
            emotions = []
            probs_list = []
            windows_info = []
            while idx < total_len:
                wsig = sig[idx: idx + win]
                if wsig.size == 0:
                    break
                f0s, energies = self._extract_window_features(wsig, sr)
                # build ML_feed-like features
                if f0s.size == 0 or energies.size == 0:
                    features = np.zeros((1, 8), dtype=np.float32)
                else:
                    feed = [
                        float(np.mean(f0s)), float(np.var(f0s)), float(np.max(f0s)), float(np.min(f0s)),
                        float(np.mean(energies)), float(np.var(energies)), float(np.max(energies)), float(np.min(energies))
                    ]
                    features = np.array(feed, dtype=np.float32).reshape(1, -1)
                # predict
                pred_label = None
                pred_probs = None
                try:
                    if model_choice == 'mlp' and hasattr(self, '_mlp_model'):
                        if hasattr(self, '_scaler_mlp'):
                            features_scaled = self._scaler_mlp.transform(features)
                        else:
                            features_scaled = features
                        probs = self._mlp_model.predict(features_scaled, verbose=0)
                        probs = probs[0] if probs.ndim > 1 else probs
                        if hasattr(self, '_le_encoder'):
                            labels = list(self._le_encoder.classes_)
                        else:
                            labels = [str(i) for i in range(probs.shape[0])]
                        pred_idx = int(np.argmax(probs))
                        pred_label = labels[pred_idx]
                        pred_probs = dict(zip(labels, [float(x) for x in probs]))
                    elif model_choice == 'knn' and hasattr(self, '_knn_model'):
                        if hasattr(self._knn_model, 'predict_proba'):
                            probs = self._knn_model.predict_proba(features)[0]
                            labels = list(self._le_encoder.classes_) if hasattr(self, '_le_encoder') else [str(i) for i in range(len(probs))]
                            pred_probs = dict(zip(labels, [float(x) for x in probs]))
                            pred_label = labels[int(np.argmax(probs))]
                        else:
                            pred_raw = self._knn_model.predict(features)[0]
                            if hasattr(self, '_le_encoder'):
                                pred_label = self._le_encoder.inverse_transform([pred_raw])[0]
                            else:
                                pred_label = str(pred_raw)
                            pred_probs = None
                    else:
                        # fallback: use energy-based heuristic
                        avg_rms = float(np.mean(energies)) if energies.size else 0.0
                        if avg_rms < 0.02:
                            pred_label = 'neutral'
                        elif avg_rms < 0.08:
                            pred_label = 'calm'
                        else:
                            pred_label = 'excited'
                        pred_probs = {pred_label: 1.0}
                except Exception as e:
                    pred_label = 'error'
                    pred_probs = {'error': 1.0}
                # record
                t_start = idx / float(sr)
                t_end = min(total_sec, (idx + win) / float(sr))
                window_predictions.append(pred_label)
                probs_list.append(pred_probs)
                windows_info.append({'start': t_start, 'end': t_end, 'label': pred_label, 'probs': pred_probs})
                idx += hop

            # aggregate durations
            duration_map = {}
            prob_accum = {}
            for w in windows_info:
                lbl = w['label']
                dur = max(0.0, w['end'] - w['start'])
                duration_map[lbl] = duration_map.get(lbl, 0.0) + dur
                if w.get('probs'):
                    for k, v in (w['probs'] or {}).items():
                        prob_accum.setdefault(k, []).append(float(v))
            # compute percentages
            summary = {}
            for lbl, dur in duration_map.items():
                pct = (dur / total_sec) * 100.0 if total_sec > 1e-6 else 0.0
                avg_prob = float(np.mean(prob_accum.get(lbl, [1.0]))) if prob_accum.get(lbl) else None
                summary[lbl] = {'duration_s': round(dur, 3), 'pct': round(pct, 2), 'avg_prob': (round(avg_prob, 4) if avg_prob is not None else None)}
            result['ok'] = True
            result['timeline'] = windows_info
            result['summary'] = summary
            return result
        except Exception as e:
            result['error'] = str(e)
            return result

    def _onAnalysisComplete(self, res, file_path):
        """Callback on main thread after analysis completes."""
        try:
            if not isinstance(res, dict) or not res.get('ok'):
                err = res.get('error') if isinstance(res, dict) else str(res)
                self.playbackStatus.setText(f"Analysis failed: {err}")
                logger.error(f"Audio analysis failed: {err}")
                return
            summary = res.get('summary', {})
            # pick top emotion by duration
            if summary:
                top = max(summary.items(), key=lambda kv: kv[1]['duration_s'])
                top_label, top_info = top
                self.playbackStatus.setText(f"Top emotion: {top_label} ({top_info['pct']}%)")
                logger.info(f"Analysis summary for {file_path}:")
                for lbl, info in summary.items():
                    logger.info(
                        "  %s — %.2fs (%.2f%%) avg_prob=%s" % (lbl, info['duration_s'], info['pct'], info['avg_prob'])
                    )
            else:
                self.playbackStatus.setText("No emotions detected")
                logger.info(f"Analysis produced empty summary for {file_path}")
        except Exception as e:
            logger.error(f"Error in _onAnalysisComplete: {e}")
            self.playbackStatus.setText("Analysis error")

    # replace placeholder _analyzeAudio with real implementation
    def _analyzeAudio(self):
        """Start background analysis for the current audio file."""
        file_path = self.selectedFileLabel.text()
        if not file_path or file_path == 'No file selected' or not os.path.exists(file_path):
            self.playbackStatus.setText('Please select or record an audio file first')
            return
        # ask which model is active
        if getattr(self, '_activeModel', None) == Model.MLP:
            if not _tensorflow_available:
                self.playbackStatus.setText('MLP model unavailable: TensorFlow not loaded')
                logger.error("MLP model unavailable: TensorFlow DLL load failed")
                return
            model_choice = 'mlp'
        else:
            model_choice = 'knn'
        self.playbackStatus.setText('Analyzing audio...')
        # run analysis in background and call back on completion
        threadPool.start(
            self._run_analysis, file_path, model_choice, callback=lambda res: self._onAnalysisComplete(res, file_path)
        )

    def onCreate(self) -> None:
        self.parent.topBar.setMode(TopBarMode.EMPTY)

    def onResume(self) -> None:
        self.parent.topBar.setMode(TopBarMode.EMPTY)

    def _updatePlaybackPosition(self):
        """Called periodically by timer to move the waveform playback cursor."""
        try:
            pos = getattr(self, '_playbackPosition', 0.0)
            # only update if waveform widget exists
            if hasattr(self, 'waveformWidget') and self.waveformWidget is not None:
                # ensure numeric value
                try:
                    pos_val = float(pos)
                except Exception:
                    pos_val = 0.0
                # update waveform cursor (safe no-op if widget not ready)
                self.waveformWidget.update_position(pos_val)
        except Exception:
            # keep silent to avoid timer exceptions crashing UI
            pass

    def _updateVuMeter(self):
        """Timer-driven UI update for VU meter (main thread)."""
        try:
            with self._vu_lock:
                level = float(getattr(self, '_vu_level', 0.0))
            # produce two lively bars with small independent jitter
            rng = np.random.RandomState(int(time() * 1000) & 0xFFFF)
            bars = []
            for i in range(self.vuWidget.num_bars):
                jitter = 0.2 * rng.rand()  # small variation per bar
                factor = 0.7 + jitter      # baseline visible range
                bars.append(max(0.0, min(1.0, level * factor)))
            self.vuWidget.update_levels(bars)
        except Exception:
            pass

    def _onModelSelected(self, model: Model):
        """Mark selected model button as active (radio behavior) and store active model."""
        try:
            logger.debug(f"Model selected: {model.name}")
            self._activeModel = model
            for m, btn in self._modelButtonMap.items():
                logger.debug(f"Updating button for model: {m.name}")
                if m == model:
                    logger.debug(f"Marking button as active for model: {m.name}")
                    btn.setChecked(True)
                    btn.setStyleSheet(primaryButton.update(
                        backgroundColor='#E95525',
                        color='#FFFFFF',
                        fontWeight='600',
                        radius=10,
                        hoverColor='#C15532',
                    ).qss)
                else:
                    logger.debug(f"Marking button as inactive for model: {m.name}")
                    btn.setChecked(False)
                    btn.setStyleSheet(secondaryButton.update(
                        backgroundColor='#353A42',
                        color='#CCCCCC',
                        border='1px solid #454A52',
                        fontWeight='500',
                        radius=10,
                        hoverColor='#3A3F47',
                    ).qss)
        except Exception as e:
            logger.error(f"Error in _onModelSelected: {e}")
