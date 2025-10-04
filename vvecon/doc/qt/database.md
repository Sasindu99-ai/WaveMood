## Database

`vvecon.qt.db.Database` is a thin wrapper around SQLAlchemy for quick local persistence.

### Usage
```python
from sqlalchemy import Column, Integer, String
from vvecon.qt.db import Database

db = Database('app.db')

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

db.create_all()

# CRUD via db.session
u = User(name='Ada')
db.session.add(u)
db.session.commit()
```

The engine is `sqlite:///app.db`. For advanced configs, create your own engine/session.


