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
    order = relationship('Order', back_populates='customer')
    success = Column(Boolean)
    message = Column(String(256))


class Inventory(Persisted):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    inventory_orders = relationship('InventoryOrder', uselist=True, back_populates='inventory')
    orders = relationship('Order', uselist=True, secondary='inventory_orders', overlaps='inventory_orders')
    success = Column(Boolean)
    message = Column(String(256))


class Order(Persisted):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False, server_default=func.now())
    customer = relationship('Customer', back_populates='order')
    inventory_orders = relationship('InventoryOrder', uselist=True, back_populates='order', overlaps='orders')
    inventory = relationship('Inventory', uselist=True, secondary='inventory_orders', overlaps='inventory_orders,orders')
    success = Column(Boolean)
    message = Column(String(256))

class InventoryOrder(Persisted):
    __tablename__ = 'inventory_orders'
    inventory_id = Column(Integer, ForeignKey('inventory.id', ondelete='CASCADE'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    inventory = relationship('Inventory', back_populates='inventory_orders', overlaps='inventory,orders')
    order = relationship('Order', back_populates='inventory_orders', overlaps='inventory,orders')
    success = Column(Boolean)
    message = Column(String(256))