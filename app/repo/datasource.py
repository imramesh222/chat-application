from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from app.settings import settings
import logging

# Simple logger setup (replace with your loggerutil if available)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Base(DeclarativeBase):
    pass

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DataSource(metaclass=Singleton):
    def __init__(self):
        try:
            self.engine = create_engine(settings.DATABASE_URL, pool_size=20, max_overflow=30, pool_timeout=60, pool_recycle=3600)
            self.ping()
            self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        except Exception as e:
            logger.exception(f"Database connection error: {e}")
            exit(1)

    def ping(self):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                logger.info(f"Database connection established: {result.scalar()}")
        except Exception as e:
            logger.exception(f"Database connection error: {e}")

    def get_session(self) -> Session:
        return self.Session()

    def close_session(self, session: Session):
        if session:
            session.close()

    def create_or_migrate_tables(self):
        try:
            self.create_tables()
            self.migrate_tables()
        except OperationalError as e:
            logger.exception(f"Error managing tables: {e}")
            exit(1)

    def create_tables(self):
        try:
            if not self.check_tables_exist():
                Base.metadata.create_all(bind=self.engine)
                logger.info("Tables created successfully.")
            else:
                logger.info("Tables already exist.")
        except OperationalError as e:
            logger.exception(f"Error creating tables: {e}")
            exit(1)

    def migrate_tables(self):
        try:
            inspector = inspect(self.engine)
            for table in Base.metadata.tables.values():
                if table.name in inspector.get_table_names():
                    logger.info(f"Table '{table.name}' exists. Checking for schema changes...")
                    self.add_columns_if_needed(table)
            logger.info("Tables migration completed successfully.")
        except OperationalError as e:
            logger.exception(f"Error migrating tables: {e}")
            exit(1)

    def check_tables_exist(self):
        try:
            inspector = inspect(self.engine)
            return len(inspector.get_table_names()) > 0
        except OperationalError:
            return False

    def add_columns_if_needed(self, table):
        try:
            inspector = inspect(self.engine)
            existing_columns = {col['name'] for col in inspector.get_columns(table.name)}
            with self.engine.connect() as connection:
                for column in table.columns:
                    if column.name not in existing_columns:
                        column_type = column.type.compile(dialect=self.engine.dialect)
                        alter_stmt = f'ALTER TABLE "{table.name}" ADD COLUMN {column.name} {column_type}'
                        logger.info(f"Executing: {alter_stmt}")
                        connection.execute(text(alter_stmt))
                        logger.info(f"Column '{column.name}' added to table '{table.name}'.")
        except Exception as e:
            logger.exception(f"Error adding columns to table '{table.name}': {e}")

class Repo:
    def __init__(self, db: DataSource):
        self.db = db
        self.logger = logging.getLogger(self.__class__.__name__)