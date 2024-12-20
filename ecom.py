from sqlalchemy import String, DateTime, func, select, ForeignKey, Float, Column, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from typing import List, Optional
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+mysqlconnector://root:root@localhost/ecomm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

order_product = Table(
    "order_product",
    Base.metadata,
    Column('user_id',ForeignKey('users.user_id')),
    Column('order_id',ForeignKey('order.order_id')),
    Column('product_id', ForeignKey('products.product_id')),
)

class Users(Base):
    __tablename__='users'
        
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    
    order: Mapped[List["Orders"]] = relationship(secondary=order_product,back_populates="users")
    
class Orders(Base):
    __tablename__='order'
        
    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[str] = mapped_column(DateTime, default=func.now())
    #user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    
    users: Mapped[List["Users"]] = relationship(secondary=order_product,back_populates="order")
    products: Mapped[List["Products"]] = relationship(secondary=order_product,back_populates="order",overlaps="order,users")

    
class Products(Base):
    __tablename__='products'
        
    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float(2))
    
    order: Mapped[List["Orders"]] = relationship(secondary=order_product,back_populates="products",overlaps="order,users")

class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Users

class OrdersSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Orders

class ProductsSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Products

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)
product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)

with app.app_context():
    db.create_all()
