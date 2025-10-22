from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session,sessionmaker
from app.config import settings
from app.models import Base
engine = create_engine(settings.DB_URL)

SessionLocal = sessionmaker(bind=engine,class_=Session)


def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def clear_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind = engine)


