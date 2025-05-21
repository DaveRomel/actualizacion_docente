from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer
from config.db import engine, meta_data

# Guarda información de cada materia y su límite de inscripciones.

inscripciones = Table("inscripciones", meta_data,
              Column("id",Integer, primary_key=True),
              Column("usuario_id",Integer, nullable=False),
              Column("materia_id",Integer ,nullable=False))

meta_data.create_all(engine)