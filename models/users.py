from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data

users = Table("users", meta_data,
              Column("id",Integer, primary_key=True),
              Column("status",Integer, nullable=False),
              Column("name",String(30), nullable=False),
              Column("email",String(20) ,nullable=False),
              Column("celular",String(10), nullable=False),
              Column("username",String(10), nullable=False),
              Column("user_passw",String(10), nullable=False),
              Column("procedencia",String(50),nullable=False))

meta_data.create_all(engine)