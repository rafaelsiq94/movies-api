from sqlalchemy import func
from typing import List, Dict

from database.models import Movie, Producer, movie_producer_association
from database import Session


def get_movies() -> List[Dict]:
    session = Session()
    movies = session.query(Movie).all()
    movies_list = [movie.serialize() for movie in movies]
    session.close()

    return movies_list


def get_max_min_win_interval_for_producers() -> Dict:
    producers = get_producers_with_more_than_one_winner_movie()
    min_producers = []
    max_producers = []

    for producer in producers:
        producer.movies.sort(key=lambda movie: movie.year)

        intervals = []
        previous_win_year = None
        for movie in producer.movies:
            if previous_win_year:
                interval = movie.year - previous_win_year
                intervals.append(interval)
            previous_win_year = movie.year

        min_interval = min(intervals)
        max_interval = max(intervals)

        min_producers.append({
            "producer": producer.name,
            "interval": min_interval,
            "previousWin": previous_win_year - min_interval,
            "followingWin": previous_win_year
        })

        max_producers.append({
            "producer": producer.name,
            "interval": max_interval,
            "previousWin": previous_win_year - max_interval,
            "followingWin": previous_win_year
        })

    min_interval = min(min_producers, key=lambda producer: producer["interval"])["interval"]
    max_interval = max(max_producers, key=lambda producer: producer["interval"])["interval"]

    return {
        "min": [
            producer
            for producer in min_producers
            if producer["interval"] == min_interval
        ],
        "max": [
            producer
            for producer in max_producers
            if producer["interval"] == max_interval
        ],
    }


def get_producers_with_more_than_one_winner_movie() -> List[Producer]:
    session = Session()
    producers = (
        session.query(Producer)
        .join(Producer.movies)
        .filter(Movie.winner)
        .group_by(Producer.id)
        .having(func.count(Movie.id) > 1)
        .all()
    )
    for producer in producers:
        winner_movies = (
            session.query(Movie)
            .join(movie_producer_association)
            .filter(movie_producer_association.c.producer_id == producer.id)
            .filter(Movie.winner)
            .all()
        )
        producer.movies = winner_movies
    session.close()

    return producers
