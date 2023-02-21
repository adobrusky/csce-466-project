from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, func, Boolean
from sqlalchemy.orm import relationship
from Database.database import Persisted

class Customer(Persisted):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    address = Column(String(256), nullable=False)
    city = Column(String(256), nullable=False)
    state = Column(String(256))
    postal_code = Column(String(256), nullable=False)
    country = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False)
    transaction = relationship('Transaction', back_populates='customer')
    success = Column(Boolean)
    message = Column(String(256))


class Product(Persisted):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    product_transactions = relationship('ProductTransaction', uselist=True, back_populates='product')
    transactions = relationship('Transaction', uselist=True, secondary='product_transactions', overlaps='product_transactions')
    success = Column(Boolean)
    message = Column(String(256))


class Transaction(Persisted):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False, server_default=func.now())
    customer = relationship('Customer', back_populates='transaction')
    product_transactions = relationship('ProductTransaction', uselist=True, back_populates='transaction', overlaps='transactions')
    products = relationship('Product', uselist=True, secondary='product_transactions', overlaps='product_transactions,transactions')
    success = Column(Boolean)
    message = Column(String(256))

class ProductTransaction(Persisted):
    __tablename__ = 'product_transactions'
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    product = relationship('Product', back_populates='product_transactions', overlaps='products,transactions')
    transaction = relationship('Transaction', back_populates='product_transactions', overlaps='products,transactions')
    success = Column(Boolean)
    message = Column(String(256))