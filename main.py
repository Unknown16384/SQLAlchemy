import sqlalchemy as db
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated, Optional

class Connection:
    def __init__(self, sql_type, **args):
        self.sql_type = sql_type
        self.args = args
    def engine(self):
        if self.sql_type == 'SQLite': return db.create_engine(f'sqlite:///{self.args['db_name']}.db')
        elif self.sql_type == 'PostgreSQL': return db.create_engine(f'postgresql://{self.args['user']}:{self.args['password']}@{self.args['server']}:{str(self.args['port'])}/{self.args['db_name']}')
        else: raise TypeError('Соединение не поддерживается')
class BaseTable(DeclarativeBase):
    __abstract__ = True
    base_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
class Orders(BaseTable):
    __tablename__ = 'Orders'
    ID: Mapped[BaseTable.base_id]
    Product_ID: Mapped[int] = mapped_column(db.ForeignKey('Products.ID'))
    Supplier_ID: Mapped[int] = mapped_column(db.ForeignKey('Suppliers.ID'))
class Suppliers(BaseTable):
    __tablename__ = 'Suppliers'
    ID: Mapped[BaseTable.base_id]
    Name: Mapped[str]
    Foo: Mapped[Optional[str]]
class Products(BaseTable):
    __tablename__ = 'Products'
    ID: Mapped[BaseTable.base_id]
    Name: Mapped[str]
    Quantity: Mapped[int]

#engine = Connection('PostgreSQL', server='localhost', port=5433, user='postgres', password='', db_name='database').engine()
engine = Connection(sql_type='SQLite', db_name='mydb').engine()
BaseTable.metadata.create_all(engine)