from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Bet(Base):
    __tablename__ = 'bets'

    id = Column(Integer, primary_key=True)
    race_id = Column(Integer, nullable=False)
    bet_on = Column(Integer, nullable=False)
    payment_id = Column(String(32), nullable=False)
    amount = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Bet %r>' % (self.id)


class Winner(Base):
    __tablename__ = 'Winners'

    id = Column(Integer, primary_key=True)
    race_id = Column(Integer, nullable=False)
    winner = Column(Integer, nullable=False)
    pot = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Race %d won by Turtle %d, splitting a pot worth %d>' % (self.race_id,self.winner, self.pot)