from sqlalchemy import (
    create_engine,
    select,
)
from sqlalchemy.orm import Session

from models import (
    Address,
    Base,
    User,
)

engine = create_engine('sqlite://', echo=True)

Base.metadata.create_all(engine)

# Create Objects and Persist
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

# Simple SELECT
with Session(engine) as session:
    stmt = select(User).where(User.name.in_(['spongebob', 'sandy']))

    for user in session.scalars(stmt):
        print(user)

with Session(engine) as session:
    # SELECT with JOIN
    stmt = (
        select(Address)
        .join(Address.user)
        .where(User.name == 'sandy')
        .where(Address.email_address == 'sandy@sqlalchemy.org')
    )
    sandy_address = session.scalars(stmt).one()
    print(sandy_address)

    # Make Changes
    stmt = select(User).where(User.name == 'patrick')
    patrick = session.scalars(stmt).one()

    patrick.addresses.append(
        Address(email_address='patrickstar@sqlalchemy.org')
    )
    sandy_address.email_address = 'sandy_cheeks@sqlalchemy.org'
    session.commit()

    # Some Deletes
    sandy = session.get(User, 2)
    sandy.addresses.remove(sandy_address)
    session.flush() # Emite o SQL, mas sem comitar a transação.

    # O objeto `patrick` expirou por causa do commit passado.
    # Daí, a referência ao patrick força a recarga do objeto, ou seja
    # a execução de um SELECT (na verdade dois: um pro usuário e outro
    # para os endereços de email).
    session.delete(patrick)
    session.commit()
    # A partir daqui, o SQL do comando DELETE e do commit é emitido.
