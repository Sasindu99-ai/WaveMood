from enums import Theme, Locale
from vvecon.qt.res import Theme as ThemeMeta, ColorTheme, Images, LocaleBuilder

__all__ = ['AppTheme']


class AppTheme(ThemeMeta):
    colorTheme = Theme.LIGHT
    colorPalette = {
        Theme.LIGHT: ColorTheme(
            primary="#4CAF50",
            secondary="#FF9800",
            background="#FFFFFF",
            text="#212121",
            accent="#03A9F4",
            error="#F44336",
            warning='#FF9800',
        ),
        Theme.DARK: ColorTheme(
            primary="#4CAF50",
            secondary="#FF9800",
            background="#121212",
            text="#E0E0E0",
            accent="#03A9F4",
            error="#F44336",
            warning='#FF9800',
        ),
    }
    colors = colorPalette[colorTheme]

    imageTheme = Theme.LIGHT
    images = Images(
        theme=Theme.LIGHT,
        default=Theme.LIGHT,
        logo='wavemood.jpg',
        mlp='mlp.png',
        knn='knn.png',
        recording='recording.gif',
    )

    locale = LocaleBuilder(locale= Locale.enUS, default=Locale.enUS)
