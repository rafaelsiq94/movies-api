import csv
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config.settings as settings
from database.models import Movie, Producer, Studio, Base

engine = create_engine(settings.DB_URI)
Session = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)
    csv_to_sqlite()


def csv_to_sqlite() -> None:
    session = Session()

    with open(settings.CSV_FILE, "r") as file:
        csv_reader = csv.reader(file, delimiter=";")
        next(csv_reader)
        for row in csv_reader:
            year, title, studios_str, producers_str, winner = row

            is_winner = winner.lower() == "yes"

            studios = [studio.strip() for studio in re.split(r',| and ', studios_str) if studio.strip()]
            producers = [producer.strip() for producer in re.split(r',| and ', producers_str) if producer.strip()]

            movie_producers = []
            for producer_name in producers:
                producer = session.query(Producer).filter_by(name=producer_name).first()
                if not producer:
                    producer = Producer(name=producer_name)
                    session.add(producer)
                movie_producers.append(producer)

            movie_studios = []
            for studio_name in studios:
                studio = session.query(Studio).filter_by(name=studio_name).first()
                if not studio:
                    studio = Studio(name=studio_name)
                    session.add(studio)
                movie_studios.append(studio)

            existing_movie = session.query(Movie).filter_by(title=title, year=year).first()
            if not existing_movie:
                movie = Movie(
                    year=year,
                    title=title,
                    winner=is_winner
                )
                movie.producers = movie_producers
                movie.studios = movie_studios
                session.add(movie)

    session.commit()
    session.close()
