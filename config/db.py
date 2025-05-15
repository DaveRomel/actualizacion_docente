from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv

load_dotenv()
#engine = create_engine("mysql+pymysql://root:@localhost:3306/storedb2")
engine = create_engine("mysql+pymysql://" + os.getenv("USER") + ":@" + os.getenv("DATABASE_HOST") + ":" + os.getenv("DATABASE_PORT") + "/" + os.getenv("DATABASE_NAME"))
meta_data = MetaData()
