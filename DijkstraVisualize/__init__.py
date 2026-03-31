from flask import Blueprint

dijkstra_bp = Blueprint('Dijkstra-Visualize', __name__, url_prefix='/Dijkstra-Visualize')

from . import views