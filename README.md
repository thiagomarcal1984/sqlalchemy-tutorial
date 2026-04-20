# ORM Quickstart
https://docs.sqlalchemy.org/en/21/orm/quickstart.html

## Declare Models
https://docs.sqlalchemy.org/en/21/orm/quickstart.html#declare-models

```python
# models.py
from typing import (
    List,
    Optional,
)
from sqlalchemy import (
    create_engine,
    ForeignKey,
    String, 
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

engine = create_engine('sqlite://', echo=True)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user_account'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List['Address']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )
    
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = 'address'
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user_account.id'))
    
    user: Mapped['User'] = relationship(back_populates='addresses')

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
```

## Create an Engine
https://docs.sqlalchemy.org/en/21/orm/quickstart.html#create-an-engine

Criaremos a engine em `main.py`:
```python
# main.py
from sqlalchemy import create_engine

engine = create_engine('sqlite://', echo=True)
```

## Emit CREATE TABLE DDL
https://docs.sqlalchemy.org/en/21/orm/quickstart.html#emit-create-table-ddl

No arquivo `main.py` usamos o método `create_all` da base class importada de `models.py`:
```python
# main.py
from sqlalchemy import create_engine
from models import (
    Address,
    Base,
    User,
)

engine = create_engine('sqlite://', echo=True)

models.Base.metadata.create_all(engine)
```

Ao executar `main.py`, temos:
```SQL
>>> import main
2026-04-19 19:07:05,286 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-19 19:07:05,287 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("user_account")
2026-04-19 19:07:05,287 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-19 19:07:05,288 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("user_account")
2026-04-19 19:07:05,288 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-19 19:07:05,288 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("address")
2026-04-19 19:07:05,288 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-19 19:07:05,289 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("address")
2026-04-19 19:07:05,289 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-19 19:07:05,290 INFO sqlalchemy.engine.Engine
CREATE TABLE user_account (
        id INTEGER NOT NULL,
        name VARCHAR(30) NOT NULL,
        fullname VARCHAR,
        PRIMARY KEY (id)
)


2026-04-19 19:07:05,290 INFO sqlalchemy.engine.Engine [no key 0.00034s] ()
2026-04-19 19:07:05,291 INFO sqlalchemy.engine.Engine
CREATE TABLE address (
        id INTEGER NOT NULL,
        email_address VARCHAR NOT NULL,
        user_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user_account (id)
)


2026-04-19 19:07:05,291 INFO sqlalchemy.engine.Engine [no key 0.00029s] ()
2026-04-19 19:07:05,292 INFO sqlalchemy.engine.Engine COMMIT
>>>
```
## Create Objects and Persist
https://docs.sqlalchemy.org/en/21/orm/quickstart.html#create-objects-and-persist

As seguintes mudanças em `main.py` foram feitas:
```python
# main.py
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import (
    Address,
    Base,
    User,
)

engine = create_engine('sqlite://', echo=True)

Base.metadata.create_all(engine)

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
```

Ao executar `main.py`, temos:
```SQL
-- Resto da saída.

2026-04-19 19:18:43,210 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-19 19:18:43,212 INFO sqlalchemy.engine.Engine INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
2026-04-19 19:18:43,212 INFO sqlalchemy.engine.Engine [generated in 0.00013s (insertmanyvalues) 1/3 (ordered; batch not supported)] ('spongebob', 'Spongebob Squarepants')
2026-04-19 19:18:43,213 INFO sqlalchemy.engine.Engine INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
2026-04-19 19:18:43,214 INFO sqlalchemy.engine.Engine [insertmanyvalues 2/3 (ordered; batch not supported)] ('sandy', 'Sandy Cheeks')
2026-04-19 19:18:43,215 INFO sqlalchemy.engine.Engine INSERT INTO user_account (name, fullname) VALUES (?, ?) RETURNING id
2026-04-19 19:18:43,215 INFO sqlalchemy.engine.Engine [insertmanyvalues 3/3 (ordered; batch not supported)] ('patrick', 'Patrick Star')
2026-04-19 19:18:43,217 INFO sqlalchemy.engine.Engine INSERT INTO address (email_address, user_id) VALUES (?, ?) RETURNING id
2026-04-19 19:18:43,218 INFO sqlalchemy.engine.Engine [generated in 0.00014s (insertmanyvalues) 1/3 (ordered; batch not supported)] ('spongebob@sqlalchemy.org', 1)
2026-04-19 19:18:43,218 INFO sqlalchemy.engine.Engine INSERT INTO address (email_address, user_id) VALUES (?, ?) RETURNING id
2026-04-19 19:18:43,218 INFO sqlalchemy.engine.Engine [insertmanyvalues 2/3 (ordered; batch not supported)] ('sandy@sqlalchemy.org', 2)
2026-04-19 19:18:43,218 INFO sqlalchemy.engine.Engine INSERT INTO address (email_address, user_id) VALUES (?, ?) RETURNING id
2026-04-19 19:18:43,219 INFO sqlalchemy.engine.Engine [insertmanyvalues 3/3 (ordered; batch not supported)] ('sandy@squirrelpower.org', 2)
2026-04-19 19:18:43,220 INFO sqlalchemy.engine.Engine COMMIT
>>>
```
## Simple SELECT
Executando o comando a seguir no interpretador, conseguimos visualizar os usuários do Spongebob e Sandy:

```python
# main.py
from sqlalchemy import (
    create_engine,
    select,
)
# Resto do código

with Session(engine) as session:
    stmt = select(User).where(User.name.in_(['spongebob', 'sandy']))

    for user in session.scalars(stmt):
        print(user)
```

Ao executar `main.py`, temos:
```SQL
-- Resto da saída.

2026-04-19 19:25:36,765 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-19 19:25:36,771 INFO sqlalchemy.engine.Engine SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name IN (?, ?)
2026-04-19 19:25:36,772 INFO sqlalchemy.engine.Engine [generated in 0.00126s] ('spongebob', 'sandy')  

    User(id=1, name='spongebob', fullname='Spongebob Squarepants')
    User(id=2, name='sandy', fullname='Sandy Cheeks')

2026-04-19 19:25:36,790 INFO sqlalchemy.engine.Engine ROLLBACK
```

## Selectd with JOIN
https://docs.sqlalchemy.org/en/21/orm/quickstart.html#select-with-join

Conseguimos recuperar o usuário da Sandy usando os métodos `select` e `join`:

```python
# main.py
# Resto do código
with Session(engine) as session:
    stmt = (
        select(Address) # Destaque neste join.
        .join(Address.user) # Destaque neste join.
        .where(User.name == 'sandy')
        .where(Address.email_address == 'sandy@sqlalchemy.org')
    )
    sandy_address = session.scalars(stmt).one()
    print(sandy_address)
```

Ao executar `main.py`, temos:
```SQL
-- Resto da saída.

2026-04-19 19:31:15,478 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-19 19:31:15,481 INFO sqlalchemy.engine.Engine SELECT address.id, address.email_address, address.user_id
FROM address JOIN user_account ON user_account.id = address.user_id
WHERE user_account.name = ? AND address.email_address = ?
2026-04-19 19:31:15,482 INFO sqlalchemy.engine.Engine [generated in 0.00162s] ('sandy', 'sandy@sqlalchemy.org')

    Address(id=2, email_address='sandy@sqlalchemy.org')

2026-04-19 19:31:15,484 INFO sqlalchemy.engine.Engine ROLLBACK
```
## Make Changes
https://docs.sqlalchemy.org/en/21/orm/quickstart.html#make-changes

Algumas mudanças em `main.py`:
```python
# main.py
# Resto do código
with Session(engine) as session:
    #Resto do código
    stmt = select(User).where(User.name == 'patrick')
    patrick = session.scalars(stmt).one()

    patrick.addresses.append(
        Address(email_address='patrickstar@sqlalchemy.org')
    )
    sandy_address.email_address = 'sandy_cheeks@sqlalchemy.org'
    session.commit()
```

Ao executar `main.py`, temos:
```SQL
-- Resto da saída.

2026-04-19 21:11:50,832 INFO sqlalchemy.engine.Engine SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
2026-04-19 21:11:50,832 INFO sqlalchemy.engine.Engine [generated in 0.00042s] ('patrick',)

2026-04-19 21:11:50,837 INFO sqlalchemy.engine.Engine SELECT address.id AS address_id, address.email_address AS address_email_address, address.user_id AS address_user_id
FROM address
WHERE ? = address.user_id

2026-04-19 21:11:50,838 INFO sqlalchemy.engine.Engine [generated in 0.00041s] (3,)
2026-04-19 21:11:50,856 INFO sqlalchemy.engine.Engine UPDATE address SET email_address=? WHERE address.id = ?
2026-04-19 21:11:50,858 INFO sqlalchemy.engine.Engine [generated in 0.00254s] ('sandy_cheeks@sqlalchemy.org', 2)
2026-04-19 21:11:50,859 INFO sqlalchemy.engine.Engine INSERT INTO address (email_address, user_id) VALUES (?, ?)
2026-04-19 21:11:50,860 INFO sqlalchemy.engine.Engine [generated in 0.00061s] ('patrickstar@sqlalchemy.org', 3)
2026-04-19 21:11:50,861 INFO sqlalchemy.engine.Engine COMMIT
```
> Note o lazy loading ao executar o comando `patrick.addresses`: um `SELECT` é executado para recuperar os endereços de e-mail do Patrick antes de fazer a inserção do endereço de e-mail dele.

## Some Deletes
https://docs.sqlalchemy.org/en/21/orm/quickstart.html#some-deletes

```python
# main.py
# Resto do código
with Session(engine) as session:
    # Resto do código
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
```

Ao executar `main.py`, temos:
```SQL
-- Resto da saída.

2026-04-19 21:20:12,451 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-19 21:20:12,454 INFO sqlalchemy.engine.Engine SELECT user_account.id AS user_account_id, user_account.name AS user_account_name, user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
2026-04-19 21:20:12,454 INFO sqlalchemy.engine.Engine [generated in 0.00046s] (2,)

2026-04-19 21:20:12,456 INFO sqlalchemy.engine.Engine SELECT address.id AS address_id, address.email_address AS address_email_address, address.user_id AS address_user_id
FROM address
WHERE ? = address.user_id
2026-04-19 21:20:12,457 INFO sqlalchemy.engine.Engine [cached since 0.01502s ago] (2,)

-- Impressão da remoção da Sandy
2026-04-19 21:20:12,459 INFO sqlalchemy.engine.Engine DELETE FROM address WHERE address.id = ?        
2026-04-19 21:20:12,459 INFO sqlalchemy.engine.Engine [generated in 0.00039s] (2,)

-- Recarga do Patrick
2026-04-19 21:20:12,476 INFO sqlalchemy.engine.Engine SELECT user_account.id AS user_account_id, user_account.name AS user_account_name, user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
2026-04-19 21:20:12,477 INFO sqlalchemy.engine.Engine [generated in 0.00045s] (3,)

2026-04-19 21:20:12,478 INFO sqlalchemy.engine.Engine SELECT address.id AS address_id, address.email_address AS address_email_address, address.user_id AS address_user_id
FROM address
WHERE ? = address.user_id
2026-04-19 21:20:12,478 INFO sqlalchemy.engine.Engine [cached since 0.03625s ago] (3,)

-- Início do flush restante e do commit.
2026-04-19 21:20:12,479 INFO sqlalchemy.engine.Engine DELETE FROM address WHERE address.id = ?
2026-04-19 21:20:12,479 INFO sqlalchemy.engine.Engine [cached since 0.02067s ago] (4,)
2026-04-19 21:20:12,480 INFO sqlalchemy.engine.Engine DELETE FROM user_account WHERE user_account.id = ?
2026-04-19 21:20:12,480 INFO sqlalchemy.engine.Engine [generated in 0.00030s] (3,)
2026-04-19 21:20:12,481 INFO sqlalchemy.engine.Engine COMMIT
```

# ORM Mapped Class Overview
https://docs.sqlalchemy.org/en/21/orm/mapping_styles.html
