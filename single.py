import os 
from typing import Optional
from sqlalchemy import (
    create_engine,
    # ForeignKey,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    Session,
)

class Base(DeclarativeBase):
    pass

class Employee(Base):
    __tablename__ = 'employee'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[Optional[int]]

    __mapper_args__ = {
        'polymorphic_identity' : 0,
        'polymorphic_on' : 'type',
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"

class Engineer(Employee):
    engineer_name: Mapped[Optional[str]]

    __mapper_args__ = {
        'polymorphic_identity' : 1
    }
    
class Manager(Employee):
    manager_name: Mapped[Optional[str]]

    __mapper_args__ = {
        'polymorphic_identity' : 2
    }

path = 'db.sqlite'
engine = create_engine(f'sqlite:///{path}')

if os.path.exists(path):
    os.remove(path)
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    emp = Employee(name='Empregado')
    eng = Engineer(
        name = 'Djiskstra',
        engineer_name = 'Eng. Djikstra',
    )
    mng = Manager(
        name = 'Chiavenatto',
        manager_name = 'Adm. Chiavenatto',
    )
    session.add(emp)
    session.add(eng)
    session.add(mng)
    session.commit()

    print('Nomes subclasses: ')
    print(f"\t{eng.engineer_name}")
    print(f"\t{mng.manager_name}")

    print('Lista: ')
    [ print(f"\t{obj}") for obj in session.scalars(select(Employee)).all() ]
