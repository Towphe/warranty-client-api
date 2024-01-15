from sqlalchemy import Boolean, Column, Date, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, text
from sqlalchemy.orm import declarative_base, relationship
from .database import Base, Session, engine

class Addresses(Base):
    __tablename__ = 'addresses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='addresses_pkey'),
    )

    id = Column(Integer, primary_key=True)
    region = Column(String(200), nullable=False)
    city = Column(String(200), nullable=False)
    barangay = Column(String(200), nullable=False)
    street = Column(String(255), nullable=False)
    zipcode = Column(Integer, nullable=False)
    created_at = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    updated_at = Column(Date)

    customers = relationship('Customers', back_populates='address')
    users = relationship('Users', back_populates='address')


class Brands(Base):
    __tablename__ = 'brands'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='brands_pkey'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    updated_at = Column(Date)

    products = relationship('Products', back_populates='brand')


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='roles_pkey'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    updated_at = Column(Date)

    users = relationship('Users', back_populates='role')


class Stores(Base):
    __tablename__ = 'stores'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='stores_pkey'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    company = Column(String(100), nullable=False)
    created_at = Column(Date, server_default=text('CURRENT_DATE'))
    updated_at = Column(Date)


class Suppliers(Base):
    __tablename__ = 'suppliers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='suppliers_pkey'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    email = Column(String(255))
    telephone = Column(String(30))
    updated_at = Column(Date)

    products = relationship('Products', back_populates='supplier')


class Customers(Base):
    __tablename__ = 'customers'
    __table_args__ = (
        ForeignKeyConstraint(['address_id'], ['addresses.id'], name='fk_address'),
        PrimaryKeyConstraint('id', name='customers_pkey')
    )

    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(30), nullable=False)
    created_at = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    updated_at = Column(Date)

    address = relationship('Addresses', back_populates='customers')
    entries = relationship('Entries', back_populates='customer')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        ForeignKeyConstraint(['brand_id'], ['brands.id'], name='fk_brand'),
        ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], name='fk_supplier'),
        PrimaryKeyConstraint('id', name='products_pkey')
    )

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=False)
    name = Column(String(250), nullable=False)
    sku = Column(String(150))
    created_at = Column(Date, server_default=text('CURRENT_DATE'))
    updated_at = Column(Date)

    brand = relationship('Brands', back_populates='products')
    supplier = relationship('Suppliers', back_populates='products')
    variations = relationship('Variations', back_populates='product')
    entries = relationship('Entries', back_populates='product')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        ForeignKeyConstraint(['address_id'], ['addresses.id'], name='fk_address'),
        ForeignKeyConstraint(['role_id'], ['roles.id'], name='fk_role'),
        PrimaryKeyConstraint('id', name='users_pkey')
    )

    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, nullable=False)
    role_id = Column(Integer, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(30), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    updated_at = Column(Date)

    address = relationship('Addresses', back_populates='users')
    role = relationship('Roles', back_populates='users')
    statuses = relationship('Statuses', back_populates='consignee')


class Statuses(Base):
    __tablename__ = 'statuses'
    __table_args__ = (
        ForeignKeyConstraint(['consignee_id'], ['users.id'], name='fk_consignee'),
        PrimaryKeyConstraint('id', name='statuses_pkey')
    )

    id = Column(Integer, primary_key=True)
    consignee_id = Column(Integer)
    name = Column(String(50))
    is_current = Column(Boolean, server_default=text('true'))
    created_at = Column(Date, server_default=text('CURRENT_DATE'))
    updated_at = Column(Date)

    consignee = relationship('Users', back_populates='statuses')
    entries = relationship('Entries', back_populates='status')


class Variations(Base):
    __tablename__ = 'variations'
    __table_args__ = (
        ForeignKeyConstraint(['product_id'], ['products.id'], name='fk_product'),
        PrimaryKeyConstraint('id', name='variations_pkey')
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    product_id = Column(Integer, nullable=False)
    is_active = Column(Boolean, server_default=text('false'))
    updated_at = Column(Date)

    product = relationship('Products', back_populates='variations')


class Entries(Base):
    __tablename__ = 'entries'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customers.id'], name='fk_customer'),
        ForeignKeyConstraint(['product_id'], ['products.id'], name='fk_product'),
        ForeignKeyConstraint(['status_id'], ['statuses.id'], name='statuses'),
        PrimaryKeyConstraint('id', name='entries_pkey')
    )

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    status_id = Column(Integer, nullable=False)
    serialno = Column(String(100), nullable=False)
    created_at = Column(Date, server_default=text('CURRENT_DATE'))
    updated_at = Column(Date)

    customer = relationship('Customers', back_populates='entries')
    product = relationship('Products', back_populates='entries')
    status = relationship('Statuses', back_populates='entries')

Base.metadata.create_all(engine)