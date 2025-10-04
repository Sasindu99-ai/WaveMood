from vvecon.qt.contrib.styles.Button import (
    dangerButton,
    darkButton,
    primaryButton,
    secondaryButton,
    successButton,
    warningButton,
)
from vvecon.qt.contrib.styles.Common import h4, h6
from vvecon.qt.util import Style, StyleSheet

__all__ = [
	'ToastStyleScheme', 'primaryToastStyleSheet', 'darkToastStyleSheet', 'warningToastStyleSheet',
	'dangerToastStyleSheet', 'successToastStyleSheet'
]


class ToastStyleScheme(StyleSheet):
	background: Style = Style("""
	background-color: {backgroundColor}; border-radius: {borderRadius}px;
	""", **dict(backgroundColor='#242424', borderRadius=8))
	title: Style = h4
	message: Style = h6
	confirmButton: Style = primaryButton
	cancelButton: Style = secondaryButton


primaryToastStyleSheet = ToastStyleScheme()
darkToastStyleSheet = ToastStyleScheme().update(confirmButton=darkButton)
warningToastStyleSheet = ToastStyleScheme().update(confirmButton=warningButton)
dangerToastStyleSheet = ToastStyleScheme().update(confirmButton=dangerButton)
successToastStyleSheet = ToastStyleScheme().update(confirmButton=successButton)
