from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, Session, sessionmaker

__all__ = ['Database']


class Database:
    db_name: str
    engine: Engine
    Model: DeclarativeMeta
    session: Session

    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = create_engine('sqlite:///' + self.db_name, echo_pool=True)
        self.Model = declarative_base()
        self.session = sessionmaker(bind=self.engine)()

    def create_all(self) -> None:
        self.Model.metadata.create_all(self.engine)
