from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.schema import CreateSchema
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from app.infrastructure.config import get_settings

settings = get_settings()

class CustomBase:
    @declared_attr
    def __table_args__(cls):
        return {'schema': settings.DATABASE.DB_SCHEMA}
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base = declarative_base(cls=CustomBase)

def create_schema(engine):
    """Create the schema if it doesn't exist"""
    if not settings.DATABASE.DB_SCHEMA:
        return
    
    with engine.connect() as conn:
        if not conn.dialect.has_schema(conn, settings.DATABASE.DB_SCHEMA):
            conn.execute(CreateSchema(settings.DATABASE.DB_SCHEMA))
            conn.commit()
