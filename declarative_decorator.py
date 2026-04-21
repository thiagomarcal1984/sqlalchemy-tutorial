from sqlalchemy import (
    create_engine, 
    String,
)
from sqlalchemy.orm import (
    registry,
    Mapped, 
    mapped_column, 
    Session, 
)

reg = registry()

@reg.mapped
class User:
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None ]

engine = create_engine('sqlite://', echo=True)

reg.metadata.create_all(engine)

with Session(engine) as session:
    spongebob = User(
        name='spongebob',
        fullname='Spongebob Squarepants',
    )
    sandy = User(
        name='sandy',
        fullname='Sandy Cheeks',
    )
    patrick = User(name='patrick', fullname='Patrick Star')
    session.add_all([spongebob, sandy, patrick])
    session.commit()
