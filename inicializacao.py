from sqlalchemy import (
    create_engine, 
    Column, 
    ForeignKey,
    insert,
    Integer, 
    MetaData,
    select,
    String,
    Table, 
    text,
)
from typing import (
    List,
    Optional,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped, 
    mapped_column, 
    relationship,
    Session,
)

def get_engine():
    return create_engine('sqlite+pysqlite:///:memory:', echo=True)

metadata_obj = MetaData()
engine = get_engine()

user_table = Table(
    'user_account',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String, nullable=False),
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    
    addresses: Mapped[List['Address']] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey('user_account.id'))
    
    user: Mapped['User'] = relationship(back_populates='addresses')

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

# Criação via ORM
Base.metadata.create_all(engine)

# Criação via objetos Table
metadata_obj.create_all(engine)

stmt = insert(user_table).values(name='spongebob', fullname='Spongebob Squarepants')

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

# Usando uma inserção de uma lista de de dicionários:
with engine.connect() as conn:
    result = conn.execute(
        insert(user_table), # Primeiro parâmetro é a declaração
        [
            {'name' : 'sandy', 'fullname' : 'Sandy Cheeks'},
            {'name' : 'patrick', 'fullname' : 'Patrick Star'},
        ]
    )
    conn.commit()
