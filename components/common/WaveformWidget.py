import numpy as np
import pyqtgraph as pg
import soundfile as sf
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont

__all__ = ["WaveformWidget"]


class WaveformWidget(pg.PlotWidget):
    """
    WaveformWidget

    Descriptions:
        This widget displays the waveform of an audio file.

    Attributes:
        waveformLoaded: Signal to be emitted when waveform data is ready( audio_data (1d ndarray), time_points (1d ndarray), duration (float), sample_rate (int), success (bool), error_msg (str))

    Methods:
        load_waveform: Start loading the waveform - this runs in a worker thread
        show_loading: Show the loading text item
        hide_loading: Hide the loading text item
        on_waveform_loaded: Called when waveform is successfully loaded and rendered
        update_position: Update the position of the playback indicator line
    """
    waveformLoaded = pyqtSignal(object, object, float, int, bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackground("#23272F")
        self.showGrid(x=True, y=False, alpha=0.3)
        self.setMenuEnabled(False)
        self.setMouseEnabled(x=True, y=False)
        self.getPlotItem().hideButtons()
        self.setMinimumHeight(150)

        font = QFont()
        font.setPointSize(8)
        self.getAxis("bottom").setTickFont(font)
        self.getAxis("bottom").setLabel("Time (seconds)", color="#CCCCCC")
        self.getAxis("left").hide()

        # Initialize variables
        self.waveform_plot = None
        self.position_line = None
        self.audio_data = None
        self.sample_rate = None
        self.duration = 0

        # Status display for loading
        self.loading_text = pg.TextItem("Loading waveform...", color="#CCCCCC", anchor=(0.5, 0.5))
        self.loading_text.setPos(0.5, 0)
        self.addItem(self.loading_text)
        self.loading_text.hide()

        # Configure the position line (playback indicator)
        self.position_line = pg.InfiniteLine(
            pos=0,
            angle=90,
            pen=pg.mkPen(color="#E95525", width=2),
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
            error_text = pg.TextItem(f"Error: {error_msg}", color="#E95525", anchor=(0.5, 0.5))
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
            pen=pg.mkPen(color="#E95525", width=1.5)
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
                self.setXRange({center, center + view_range.width()}, padding=0.0)
