from typing import List
from sqlalchemy import (
    create_engine,
    Column,
    ForeignKey,
    select,
    Table,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)

class Base(DeclarativeBase):
    pass

aluno_curso = Table(
    'relacao_alunos_cursos',
    Base.metadata,
    Column('id_aluno', ForeignKey('alunos.id'), primary_key=True),
    Column('id_curso', ForeignKey('cursos.id'), primary_key=True),
)

class Aluno(Base):
    __tablename__ = 'alunos'
    id : Mapped[int] = mapped_column(primary_key=True)
    nome : Mapped[str]
    cursos: Mapped[List['Curso']] = relationship(
        'Curso',
        secondary=aluno_curso,
        back_populates='alunos',
    )

class Curso(Base):
    __tablename__ = 'cursos'
    id : Mapped[int] = mapped_column(primary_key=True)
    nome : Mapped[str]
    alunos: Mapped[List['Aluno']] = relationship(
        'Aluno',
        secondary=aluno_curso,
        back_populates='cursos',
    )

engine = create_engine('sqlite:///:memory:', echo=False)

Base.metadata.create_all(engine)

session = Session(engine)

aluno = Aluno(nome='Thiago')
curso = Curso(nome='Python')

aluno.cursos.append(curso)

session.add_all([aluno, curso])
session.commit()

for obj in session.scalars(select(Aluno)):
    print(obj.nome)
    for curso in obj.cursos:
        print('\t', curso.nome)
for obj in session.scalars(select(Curso)):
    print(obj.nome)
    for aluno in obj.alunos:
        print('\t', aluno.nome)

session.close()
