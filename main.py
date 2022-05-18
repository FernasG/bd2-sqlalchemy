from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'northwind'}

    categoryid = Column(Integer, primary_key=True)
    categoryname = Column(String(50))
    description = Column(String(100))


class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = {'schema': 'northwind'}

    customerid = Column(String(5), primary_key=True)
    companyname = Column(String(50))
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(50))
    city = Column(String(20))
    region = Column(String(15))
    postalcode = Column(String(9))
    country = Column(String(15))
    phone = Column(String(17))
    fax = Column(String(17))


class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'northwind'}

    employeeid = Column(Integer, primary_key=True)
    lastname = Column(String(10))
    firstname = Column(String(10))
    title = Column(String(25))
    titleofcourtesy = Column(String(5))
    birthdate = Column(DateTime)
    hiredate = Column(DateTime)
    address = Column(String(50))
    city = Column(String(20))
    region = Column(String(2))
    postalcode = Column(String(9))
    country = Column(String(15))
    homephone = Column(String(14))
    extension = Column(String(4))
    reportsto = Column(Integer)
    notes = Column(Text)


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'northwind'}

    productid = Column(Integer, primary_key=True)
    productname = Column(String(35))
    supplierid = Column(Integer, nullable=False)
    categoryid = Column(Integer, nullable=False)
    quantityperunit = Column(String(20))
    unitprice = Column(Numeric(13, 4))
    unitsinstock = Column(SmallInteger)
    unitsonorder = Column(SmallInteger)
    reorderlevel = Column(SmallInteger)
    discontinued = Column(String(1))


class Shipper(Base):
    __tablename__ = 'shippers'
    __table_args__ = {'schema': 'northwind'}

    shipperid = Column(Integer, primary_key=True)
    companyname = Column(String(20))
    phone = Column(String(14))


class Supplier(Base):
    __tablename__ = 'suppliers'
    __table_args__ = {'schema': 'northwind'}

    supplierid = Column(Integer, primary_key=True)
    companyname = Column(String(50))
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(50))
    city = Column(String(20))
    region = Column(String(15))
    postalcode = Column(String(8))
    country = Column(String(15))
    phone = Column(String(15))
    fax = Column(String(15))
    homepage = Column(String(100))


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'northwind'}

    orderid = Column(Integer, primary_key=True)
    customerid = Column(ForeignKey('northwind.customers.customerid', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    employeeid = Column(ForeignKey('northwind.employees.employeeid', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    orderdate = Column(DateTime)
    requireddate = Column(DateTime)
    shippeddate = Column(DateTime)
    freight = Column(Numeric(15, 4))
    shipname = Column(String(35))
    shipaddress = Column(String(50))
    shipcity = Column(String(15))
    shipregion = Column(String(15))
    shippostalcode = Column(String(9))
    shipcountry = Column(String(15))
    shipperid = Column(Integer)

    customer = relationship('Customer')
    employee = relationship('Employee')


class OrderDetail(Base):
    __tablename__ = 'order_details'
    __table_args__ = {'schema': 'northwind'}

    orderid = Column(ForeignKey('northwind.orders.orderid', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    productid = Column(ForeignKey('northwind.products.productid', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    unitprice = Column(Numeric(13, 4))
    quantity = Column(SmallInteger)
    discount = Column(Numeric(10, 4))

    order = relationship('Order')
    product = relationship('Product')

if __name__ == "__main__":
    connection = create_engine("postgresql://postgres:123456@localhost/postgres")
    schema = "northwind"
    meta = MetaData()
    meta.reflect(bind=connection, schema=schema)

    table_foreign_keys = {
        "orders": {"customerid": { "table": "customers" }, "employeeid": { "table": "employees" }},
        "order_details": {"orderid": { "table": "orders" }, "productid": { "table": "products" }},
        "products": {"categoryid": { "table": "categories" }, "supplierid": { "table": "suppliers" }}
    }

    for table_name in meta.tables:
        name = table_name.split(".")[1]

        if name in table_foreign_keys.keys():
            table = meta.tables[table_name].foreign_keys

            for foreign_key in table_foreign_keys[name].keys():
                keys = [key.column.name for key in table]

                if foreign_key not in keys:
                    print(f"Criando chave estrangeira: {foreign_key}")
                    attrs = table_foreign_keys[name][foreign_key]
                    sql = f"ALTER TABLE {table_name} ADD CONSTRAINT fk_{foreign_key} FOREIGN KEY ({foreign_key}) REFERENCES {schema}.{attrs['table']} ON DELETE RESTRICT ON UPDATE CASCADE"
                    try:
                        connection.execute(sql)
                        print("\033[92mChave estrangeira criada com sucesso!\033[0m")
                    except Exception as error:
                        print("\033[91mOcorreu um erro ao criar chave estrangeira!\033[0m")
