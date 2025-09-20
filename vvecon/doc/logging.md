## Logging

`vvecon.qt.logger.logger` wraps Python logging with helpful formatting including filename and line number.

### Usage
```python
from vvecon.qt.logger import logger

logger.info('App started')
logger.debug('State: %s', {'k': 1})
logger.warning('Careful')
logger.error('Oops')
logger.critical('Boom')
```

### Configuration
```python
logger.setUserName('alice')
logger.setLevel('INFO')
logger.setDestination('app.log')
```

Default format: `%(asctime)s [%(filename)s:%(lineno)d] LEVEL: | user - message`


