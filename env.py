from vvecon.qt.enums import EnvMode
from vvecon.qt.env import Env, EnvManager

__all__ = ['env']

env = EnvManager([
    Env(
		EnvMode.DEBUG,
		ENVIRONMENT='development',
        # Google Maps API Key
        GOOGLE_MAPS_API_KEY='',
	),
	Env(
		EnvMode.RELEASE,
		ENVIRONMENT='production',
        # Google Maps API Key
        GOOGLE_MAPS_API_KEY='',
	)
], default=EnvMode.DEBUG)
