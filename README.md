# Engine
https://docs.sqlalchemy.org/en/20/tutorial/engine.html

```python
from sqlalchemy import create_engine, text
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

with engine.connect() as conn:
    result = conn.execute(text("select 'Hey, world!'"))
    print(result.all())                                                                                                                                                   

# Sintaxe com a função `connect`:
with engine.connect() as conn:
    conn.execute(text("create table some_table(x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x" : 2, "y": 4}],
    )
    conn.commit()

# Sintaxe com a função `begin`:
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table VALUES(:x, :y)"),
        [{'x' : 6, 'y' : 8}, {'x': 9, 'y' : 10}],
    )

# Listando o resultado das inserções:
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM some_table")).all()
    print(result)

# Listando de acordo com a documentação: 
with engine.connect() as conn:
    # O retorno é do tipo `Result`, em esecífico um `CursorResult`.
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

# Atribuição de tuplas: tuplas preenchem várias variáveis de uma vez: 
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for x, y in result:
        print(f"X: {x}; Y: {y}")
        
# Índice de inteiros: sintaxe de chaves e índice de base 0:
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"X: {row[0]}; Y: {row[1]}")

# Nome de atributos: cada coluna correspondente a um atributo da linha:
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"X: {row.x}; Y: {row.y}")

# Acesso de mapeamento: cria um dicionário somente leitura a partir do resultado:
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    mapeamento = result.mappings() # Retorna um `MappingResult`.
    print(type(mapeamento))
    for dictio in mapeamento:
        print(f"X: {dictio.get('x')}; Y: {dictio.get('y')}")


# Usando o objeto Session do módulo `orm`
from sqlalchemy.orm import Session

stmt = text("SELECT * FROM some_table WHERE y > :y ORDER BY x, y")

with Session(engine) as session:
    result = session.execute(stmt, {'y' : 6})
    for row in result:
        print(f"x : {row.x}  y: {row.y}")

# Outro exemplo atualizando mais de um registro com Session:
with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{'x': 6, 'y': 11}, {'x': 9, 'y': 13}],
    )
    session.commit()
```
# Working with Database Metadata
https://docs.sqlalchemy.org/en/20/tutorial/metadata.html

```python
# Criando um objeto `MetaData` - ele serve como um mapeamento entre
# os nomes das tabelas e os objetos `Table` do SqlAlchemy.
from sqlalchemy import MetaData
metadata_obj = MetaData()

# Criando uma tabela `user_account` após importar os tipos Table, Column, 
# Integer e String (note que não precisamos informar o engine/querystring):
from sqlalchemy import Table, Column, Integer, String
user_table = Table(
    'user_account',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String),
)

# Exibindo informações da coluna `name`:
user_table.c.name

# Exibindo os nomes das colunas:
user_table.c.keys()

# Resgatando a chave primária da tabela:
user_table.primary_key

# Usando chave estrangeira na tabela:
from sqlalchemy import ForeignKey
address_table = Table(
    "address",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String, nullable=False),
)

# Criando as tabelas:
from sqlalchemy import create_engine, text
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
metadata_obj.create_all(engine)

# Excluindo as tabelas:
metadata_obj.drop_all(engine) 
```

## Estabelecendo uma base declarativa
https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#using-orm-declarative-forms-to-define-table-metadata
```python
# Criando a classe base:
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

# Acessando o atributo de classe `DeclarativeBase.metadata`:
Base.metadata

# Criando as classes `User` e `Address` (na linha de comando não use
# mais de uma quebra de linha por classe):
from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    
    addresses: Mapped[List['Address']] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# Declarando a classe usuário sem as anotações de tipo das colunas:
'''
class User(Base):
    __tablename__ = "user_account"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(30), nullable=False)
    fullname = mapped_column(String)

    addresses = relationship("Address", back_populates="user")

    # ... definition continues
'''
class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey('user_account.id'))
    
    user: Mapped['User'] = relationship(back_populates='addresses')

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

# Criando o usuário Sandy:
sandy = User(name='sandy', fullname='Sandy Cheeks')

# Criando as tabelas a partir da base declarativa:
from sqlalchemy import create_engine
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

Base.metadata.create_all(engine)
```
## Table Reflection (Reflexão de tabela)
https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#table-reflection

```python
# Exemplo de reflexão de tabela
some_table = Table("some_table", metadata_obj, autoload_with=engine)

# Outro exemplo, mas usando o objeto metadata de uma base declarativa:
endereco = Table('address', Base.metadata, autoload_with=engine)
```
## Refletindo todas as tabelas de uma vez só (página separada para table reflection)
https://docs.sqlalchemy.org/en/20/core/reflection.html#reflecting-all-tables-at-once

```python
# metadata_obj = MetaData()
metadata_obj = Base.metadata
metadata_obj.reflect(bind=engine)
users_table = metadata_obj.tables["user_account"]
addresses_table = metadata_obj.tables["address"]
```
# Working with Data

## Using INSERT Statements
```python
from sqlalchemy import insert
stmt = insert(user_table).values(name='spongebob', fullname='Spongebob Squarepants')
print(stmt)
'''Saída: INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)'''
# Note que a declaração (stmt) não foi compilada, por isso os parâmetros
# são precedidos de dois pontos:

compiled = stmt.compile()
compiled.params
'''Saída: {'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}'''

# Executando a declaração:

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

# Imprimndo o valor da chave primária inserida no banco:
result.inserted_primary_key
# Tupla de Saída: (1,)

# Imprimindo a declaração insert sem usar o método `values`:
print(insert(user_table))
'''Saída: INSERT INTO user_account (id, name, fullname) VALUES (:id, :name, :fullname)'''
# Note que todas as colunas da tabela são inseridas na declaração `VALUES` do SQL gerado.

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
'''
Saída:
2026-02-25 17:07:33,973 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-02-25 17:07:33,973 INFO sqlalchemy.engine.Engine INSERT INTO user_account (name, fullname) VALUES (?, ?)
2026-02-25 17:07:33,974 INFO sqlalchemy.engine.Engine [generated in 0.00106s] [('sandy', 'Sandy Cheeks'), ('patrick', 'Patrick Star')]
2026-02-25 17:07:33,974 INFO sqlalchemy.engine.Engine COMMIT
'''

# Inserção de valores default da tabela (nem todo backend de DB suporta):
print(insert(user_table).values().compile(engine))
''' Saída: INSERT INTO user_account DEFAULT VALUES '''

# Usando um `INSERT` com retorno:
insert_stmt = insert(address_table).returning(address_table.c.id, address_table.c.email_address)
print(insert_stmt)

# Inserindo dados a partir de um `select` e mostrando o SQL do `INSERT` com retorno:
select_stmt = select(user_table.c.id, user_table.c.name + '@aol.com')
insert_stmt = insert(address_table).from_select(
    ['user_id', 'email_address'],
    select_stmt,
)
print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))
```
## Using SELECT Statements
```python
# To be continued...
```
