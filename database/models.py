from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
  Table,
  Column,
  Integer,
  String,
  Boolean,
  ForeignKey
)

Base = declarative_base()

movie_producer_association = Table(
    'movie_producer_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('producer_id', Integer, ForeignKey('producers.id'))
)

movie_studio_association = Table(
    'movie_studio_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('studio_id', Integer, ForeignKey('studios.id'))
)


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    winner = Column(Boolean, default=False)
    year = Column(Integer)
    producer_id = Column(ForeignKey('producers.id'))
    studio_id = Column(ForeignKey('studios.id'))

    producers = relationship('Producer', secondary=movie_producer_association, back_populates='movies')
    studios = relationship('Studio', secondary=movie_studio_association)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'winner': self.winner,
            'year': self.year,
            'producers': [producer.name for producer in self.producers],
            'studios': [studio.name for studio in self.studios]
        }


class Producer(Base):
    __tablename__ = 'producers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    movies = relationship('Movie', secondary=movie_producer_association, back_populates='producers')


class Studio(Base):
    __tablename__ = 'studios'

    id = Column(Integer, primary_key=True)
    name = Column(String)
