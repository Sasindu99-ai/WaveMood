python -m nuitka --standalone --no-pyi-file --assume-yes-for-downloads
--jobs=8
--lto=no
--plugin-enable=pyqt6
--enable-plugins=pyqt6
--include-module=pygments.formatters.terminal256
--include-module=pygments.lexers.python
--include-data-dir=lib/res/images/0/=lib/res/images/0/
--include-data-dir=lib/res/images/1/=lib/res/images/1/
--include-data-dir=lib/res/lang=lib/res/lang
--include-data-dir=lib/res/fonts=lib/res/fonts
--include-qt-plugins=all
--include-data-dir=vvecon/qt/res/Icons=vvecon/qt/res/Icons
--include-data-dir=vvecon/qt/res/Icons/Outlined/static=vvecon/qt/res/Icons/Outlined/static
--include-data-dir=vvecon/qt/res/Icons/Rounded/static=vvecon/qt/res/Icons/Rounded/static
--include-data-dir=vvecon/qt/res/Icons/Sharp/static=vvecon/qt/res/Icons/Sharp/static
--windows-icon-from-ico=lib/res/images/logo.ico
--windows-console-mode=force
--experimental=fast-mode
--output-dir="debug" "Nevada Broadcaster.py"

python -m nuitka --standalone --no-pyi-file --assume-yes-for-downloads --jobs=8 --lto=no --plugin-enable=pyqt6 --enable-plugins=pyqt6 --include-module=pygments.formatters.terminal256 --include-module=pygments.lexers.python --include-data-dir=lib/res/images/0/=lib/res/images/0/ --include-data-dir=lib/res/images/1/=lib/res/images/1/ --include-data-dir=lib/res/lang=lib/res/lang --include-data-dir=lib/res/fonts=lib/res/fonts --include-qt-plugins=all --include-data-dir=vvecon/qt/res/Icons=vvecon/qt/res/Icons --include-data-dir=vvecon/qt/res/Icons/Outlined/static=vvecon/qt/res/Icons/Outlined/static --include-data-dir=vvecon/qt/res/Icons/Rounded/static=vvecon/qt/res/Icons/Rounded/static --include-data-dir=vvecon/qt/res/Icons/Sharp/static=vvecon/qt/res/Icons/Sharp/static --windows-icon-from-ico=lib/res/images/logo.ico --windows-console-mode=force --experimental=fast-mode --output-dir="debug" "Nevada Broadcaster.py"
