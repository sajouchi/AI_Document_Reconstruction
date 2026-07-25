from sqlmodel import Session, create_engine,select, SQLModel

# basic sqlite configs
SQL_LITE_FILE_NAME = "database.db"
SQL_LITE_URL = f"sqlite:///{SQL_LITE_FILE_NAME}"

# sqlmodel engine creation
connect_args = {"check_same_thread": False}
engine = create_engine(SQL_LITE_URL, echo=True, connect_args=connect_args)

def get_session():
        with Session(engine) as session:
            yield session
