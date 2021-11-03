from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from config import connection_db

# Local host
#connection_db = "sqlite:///basedatos.db"
connection_db = "postgresql://bsygmxcccteayr:62a8578fc9bd346db86a2c922ba6395ab874bb201a771bc8219b377119f4838c@ec2-3-226-165-74.compute-1.amazonaws.com:5432/d5b3h7qkpi5fpn"

Base = declarative_base()

engine = create_engine(connection_db)

Session = sessionmaker(bind=engine)