from flask import Blueprint, jsonify, request
from src.movie_service import get_movies, get_max_min_win_interval_for_producers

movies = Blueprint('api', __name__, url_prefix='/movies')


@movies.route('', methods=['GET'])
def get_movies_handler():
    projection = request.args.get('projection')
    if projection == 'max-min-win-interval-for-producers':
        result = get_max_min_win_interval_for_producers()
        return jsonify(result)
    else:
        movies = get_movies()
        return jsonify(movies)
