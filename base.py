from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

Base = declarative_base()

# Create an engine that stores data in the local directory's
# bot.sqlite file.
engine = create_engine('sqlite:///bot.sqlite', poolclass=NullPool)

_SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(_SessionFactory)


def transactional(func):
    def call(*args, **kwargs):
        session = Session()
        try:
            result = func(*args, **kwargs)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return result
    return call
