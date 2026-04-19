import os 
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
    type: Mapped[str]

    __mapper_args__ = {
        'polymorphic_identity' : 'employee',
        'polymorphic_on' : 'type',
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"

class Engineer(Employee):
    engineer_name: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        'polymorphic_identity' : 'engineer'
    }
    
class Manager(Employee):
    manager_name: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        'polymorphic_identity' : 'manager'
    }

path = 'db.sqlite'
engine = create_engine(f'sqlite:///{path}')

if os.path.exists(path):
    os.remove(path)
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    eng = Engineer(
        name = 'Djiskstra',
        engineer_name = 'Eng. Djikstra',
    )
    mng = Manager(
        name = 'Chiavenatto',
        manager_name = 'Adm. Chiavenatto',
    )
    session.add(eng)
    session.add(mng)
    session.commit()

    print('Nomes: ')
    print(f"\t{eng.engineer_name}")
    print(f"\t{mng.manager_name}")

    print('Lista: ')
    [ print(obj) for obj in session.scalars(select(Employee)).all() ]
