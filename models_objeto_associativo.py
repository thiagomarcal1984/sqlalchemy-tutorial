from typing import List
from sqlalchemy import (
    create_engine,
    ForeignKey,
    select,
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

class RelacaoAlunoCurso(Base):
    # Cuidado: no fim de cada linha não use vírgulas para que não sejam atribuídas tuplas!
    __tablename__ = 'relacao_alunos_cursos'
    id_aluno: Mapped[int] = mapped_column(ForeignKey('alunos.id'), primary_key=True)
    id_curso: Mapped[int] = mapped_column(ForeignKey('cursos.id'), primary_key=True)
    extra: Mapped[str | None]

    aluno: Mapped['Aluno'] = relationship(back_populates='relacoes')
    curso: Mapped['Curso'] = relationship(back_populates='relacoes')


class Aluno(Base):
    __tablename__ = 'alunos'
    id : Mapped[int] = mapped_column(primary_key=True)
    nome : Mapped[str]
    relacoes: Mapped[List['RelacaoAlunoCurso']] = relationship(
        'RelacaoAlunoCurso',
        back_populates='aluno',
    )

class Curso(Base):
    __tablename__ = 'cursos'
    id : Mapped[int] = mapped_column(primary_key=True)
    nome : Mapped[str]
    relacoes: Mapped[List['RelacaoAlunoCurso']] = relationship(
        'RelacaoAlunoCurso',
        back_populates='curso',
    )

engine = create_engine('sqlite:///:memory:', echo=False)

Base.metadata.create_all(engine)

session = Session(engine)

aluno = Aluno(nome='Thiago')
curso_python = Curso(nome='Python')
curso_java = Curso(nome='Java')

aluno.relacoes.append(RelacaoAlunoCurso(aluno=aluno, curso=curso_python))
aluno.relacoes.append(RelacaoAlunoCurso(aluno=aluno, curso=curso_java))

session.add_all([aluno, curso_python, curso_java])
session.commit()

for obj in session.scalars(select(Aluno)):
    print(obj.nome)
    for relacao in obj.relacoes:
        print('\t', relacao.curso.nome)
for obj in session.scalars(select(Curso)):
    print(obj.nome)
    for relacao in obj.relacoes:
        print('\t', relacao.aluno.nome)

session.close()
