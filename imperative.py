from sqlalchemy import (
    Column,
    create_engine,
    ForeignKey,
    Integer, 
    String, 
    Table, 
)
from sqlalchemy.orm import (
    registry,
    relationship,
    Session,
)

mapper_registry = registry()

# Primeiro as tabelas...
user_table = Table(
    'user_account',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String),
)

address_table = Table(
    'address',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user_account.id')),
    Column('email_address', String),
)

# Depois as classes de entidade...
class User:
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address:
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

# E depois os mapeamentos e as propriedades.
mapper_registry.map_imperatively(
    User, 
    user_table,
    properties = {
        'addresses' : relationship(
            Address, # Note que chamamos a classe, não a string com seu nome.
            back_populates='user',
            order_by=address_table.c.id,
        ),
    }
)

mapper_registry.map_imperatively(
    Address,
    address_table,
    properties = {
        'user' : relationship(User, back_populates='addresses')
    }
)

engine = create_engine('sqlite://', echo=True)

mapper_registry.metadata.create_all(engine)

with Session(engine) as session:
    spongebob = User(
        name='spongebob',
        fullname='Spongebob Squarepants',
        addresses=[Address(email_address='spongebob@sqlalchemy.org')],
    )
    sandy = User(
        name='sandy',
        fullname='Sandy Cheeks',
        addresses=[
            Address(email_address='sandy@sqlalchemy.org'),
            Address(email_address='sandy@squirrelpower.org'),
        ],
    )
    patrick = User(name='patrick', fullname='Patrick Star')
    session.add_all([spongebob, sandy, patrick])
    session.commit()
