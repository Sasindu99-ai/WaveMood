python -m nuitka --standalone --no-pyi-file --assume-yes-for-downloads
--jobs=8
--lto=no
--plugin-enable=pyqt6
--enable-plugins=pyqt6
--include-module=pygments.formatters.terminal256
--include-module=pygments.lexers.python
--include-data-dir=res/images/light/=res/images/light/
--include-data-dir=res/lang=res/lang
--include-data-dir=res/fonts=res/fonts
--include-data-dir=res/locale=res/locale
--include-data-dir=res/nlm=res/nlm
--include-data-dir=res/qss=res/qss
--include-qt-plugins=all
--include-data-dir=vvecon/qt/res/Icons=vvecon/qt/res/Icons
--include-data-dir=vvecon/qt/res/Icons/Outlined/static=vvecon/qt/res/Icons/Outlined/static
--include-data-dir=vvecon/qt/res/Icons/Rounded/static=vvecon/qt/res/Icons/Rounded/static
--include-data-dir=vvecon/qt/res/Icons/Sharp/static=vvecon/qt/res/Icons/Sharp/static
--windows-icon-from-ico=res/images/logo.ico
--windows-console-mode=force
--experimental=fast-mode
--output-dir="debug" "WaveMood.py"

python -m nuitka --standalone --no-pyi-file --assume-yes-for-downloads --jobs=8 --lto=no --plugin-enable=pyqt6 --enable-plugins=pyqt6 --include-module=pygments.formatters.terminal256 --include-module=pygments.lexers.python --include-data-dir=res/images/0/=res/images/0/ --include-data-dir=res/images/1/=res/images/1/ --include-data-dir=res/lang=res/lang --include-data-dir=res/fonts=res/fonts --include-data-dir=res/locale=res/locale --include-data-dir=res/nlm=res/nlm --include-data-dir=res/qss=res/qss --include-qt-plugins=all --include-data-dir=vvecon/qt/res/Icons=vvecon/qt/res/Icons --include-data-dir=vvecon/qt/res/Icons/Outlined/static=vvecon/qt/res/Icons/Outlined/static --include-data-dir=vvecon/qt/res/Icons/Rounded/static=vvecon/qt/res/Icons/Rounded/static --include-data-dir=vvecon/qt/res/Icons/Sharp/static=vvecon/qt/res/Icons/Sharp/static --windows-icon-from-ico=res/images/logo.ico --windows-console-mode=force --experimental=fast-mode --output-dir="debug" "WaveMood.py"
