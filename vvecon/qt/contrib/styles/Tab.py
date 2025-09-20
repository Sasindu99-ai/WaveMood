from vvecon.qt.util import Style

__all__ = ['basic']


basic = Style("""
QTabWidget::pane {
    border: 2px solid #ddd;
    background: #f9f9f9;
    border-radius: 8px;
}

QTabBar::tab {
    background: #ffffff;
    color: #333;
    padding: 10px 20px;
    margin: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid #ccc;
}

QTabBar::tab:selected {
    background: #0078D7;
    color: white;
    font-weight: bold;
    border: 1px solid #0078D7;
}

QTabBar::tab:hover {
    background: #0A4D8C;
    border: 1px solid #0078D7;
}

QTabBar::tab:!selected {
    background: #f2f2f2;
    color: #666;
}

QTabWidget::tab-bar {
    alignment: left;
}

/* Scroll Buttons */
QTabBar::scroller {
    width: 20px;
}

/* Scrollable Tabs */
QTabBar::tear {
    background: #ffffff;
}

/* Custom Scroll Bar */
QScrollBar:vertical {
    border: none;
    background: #f2f2f2;
    width: 8px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: #bbb;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #999;
}

QScrollBar::add-line:vertical, 
QScrollBar::sub-line:vertical {
    background: none;
    border: none;
}
""")
