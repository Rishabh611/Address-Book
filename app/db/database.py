from databases import Database
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///app/db/address.db"

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL)

Base = declarative_base()

class AddressModel(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    flat_number = Column(String, index=True)
    building_name = Column(String, index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    postal_code = Column(String, index=True)
    country = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

Base.metadata.create_all(bind=engine)

database = Database(DATABASE_URL)