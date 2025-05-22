from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data

# Guarda información de cada materia y su límite de inscripciones.

materias = Table("materias", meta_data,
              Column("id",Integer, primary_key=True),
              Column("name",String(30), nullable=False),
              Column("limite_inscritos",Integer ,nullable=False),
              Column("fecha_curso", String(10), nullable=False),
              Column("hora_inicio", String(10), nullable=False))

meta_data.create_all(engine)