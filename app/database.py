from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session,sessionmaker
from app.config import settings

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
"""from app.models import Base
Base.metadata.create_all(bind = engine)"""
