from vvecon.qt.enums import EnvMode
from vvecon.qt.env import Env, EnvManager

__all__ = ["env"]

env = EnvManager([
    Env(
		EnvMode.DEBUG,
        dotenv="dev.env",
		ENVIRONMENT="development",
        # Google Maps API Key
        GOOGLE_MAPS_API_KEY="",
	),
	Env(
		EnvMode.RELEASE,
        dotenv="prod.env",
		ENVIRONMENT="production",
        # Google Maps API Key
        GOOGLE_MAPS_API_KEY="",
	)
], default=EnvMode.DEBUG)
