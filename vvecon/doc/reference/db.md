## Database

### Database (`vvecon.qt.db.Database`)
```python
Database(db_name: str)
engine: sqlalchemy.Engine
Model: sqlalchemy.orm.DeclarativeMeta  # Base class for models
session: sqlalchemy.orm.Session

def create_all(self) -> None
```

Usage: define ORM classes by subclassing `db.Model`, then call `db.create_all()`.


