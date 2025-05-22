from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Text
from config.db import engine, meta_data

users = Table("users", meta_data,
              Column("id",Integer, primary_key=True),
              Column("status",Integer, nullable=False),
              Column("name",String(40), nullable=False),
              Column("email",String(30) ,nullable=False),
              Column("celular",String(10), nullable=False),
              Column("username",String(20), nullable=False),
              Column("user_passw",Text, nullable=False),
              Column("procedencia",String(60),nullable=False),
              Column("correoEnviado",Integer, nullable=False),
            Column("codigo_recuperacion", String(6)),)

meta_data.create_all(engine)