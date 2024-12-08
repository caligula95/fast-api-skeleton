from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
from .config import config

if(config['DATABASE_URL'] is not None):
    engine = create_engine(config['DATABASE_URL'])
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
else:
    conn_str = (f"postgresql+psycopg2://{config['DATABASE_USER']}:{config['DATABASE_PASSWORD']}@{config['DATABASE_HOST']}:"
            f"{config['DATABASE_PORT']}/{config['DATABASE_NAME']}")
    engine = create_engine(
        conn_str,
        echo=config['ECHO_QUERIES'] is True,
        echo_pool=True,
        pool_pre_ping=True,
        pool_size=config['DATABASE_POOL_SIZE'],
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    # print("Opening database session")
    with Session(engine) as session:
        # print("Session opened")
        # print(session)
        yield session
    session.close()
    # print("Session closed")
    # print(session)