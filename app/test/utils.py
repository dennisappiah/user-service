from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Dependency override for the database session (mocking response of db)
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency override for the current user
def override_get_current_user():
    return {"username": "dennisappiah", "id": 1, "user_role": "admin"}
