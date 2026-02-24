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
# To be continued.
```
