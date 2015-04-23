# sample program for thinkful python course

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship

engine = create_engine('###')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    bids = relationship("Bid", backref="item")
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    items = relationship("Item", backref="user")
    bids = relationship("Bid", backref="user")

class Bid(Base):
    __tablename__ = "bid"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

joe = User(username='joe', password='joe')
apple = User(username='apple', password='apple')
genie = User(username='genie', password='genie')

baseball = Item(name='BaseBall', description='Legit BaseBall', user=joe)
apple_bid = Bid(price=10000.00, item=baseball, user=apple)
genie_bid = Bid(price=10000.99, item=baseball, user=genie)

session.add_all([joe, apple, genie, baseball, apple_bid, genie_bid])
session.commit()

row = session.query(User.username, Item.name).join(Bid, Item).filter(Item.name == "BaseBall").order_by(Bid.price).all()
highest_bidder = row[-1].username
print highest_bidder
