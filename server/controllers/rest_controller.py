from flask import Flask, jsonify, request, json, make_response
from time import time
from server.controllers.controller_interface import ControllerInterface


class RestController(ControllerInterface):
    """Initialize flask routes for non gate related routes, like data host for graphs."""
    clients = []

    def __init__(self, water_repository, storm_repository):
        self.water_repository = water_repository
        self.storm_repository = storm_repository

    app = Flask(__name__)

    def add_routes(self, app):
        """Add routes to flask in app.py."""
        app.add_endpoint('/establish', 'establish', self.handle_establish_request)
        app.add_endpoint('/alive', 'alive', self.handle_alive_request)
        app.add_endpoint('/water', 'water', self.handle_water_request)
        app.add_endpoint('/storm', 'storm', self.handle_storm_request)
        app.add_endpoint('/db-fetch', 'db-fetch', self.handle_dbfetch_request)

    def handle_establish_request(self):
        """Save client address and send connection established response back."""
        self.clients.append(request.remote_addr)
        return jsonify({
            'connection established': True,
            'timestamp': time()
        })

    def handle_alive_request(self):
        """Reply to alive request with True and current time."""
        return jsonify({
            'alive': True,
            'timestamp': time()
        })

    def handle_water_request(self):
        """Host JSON graph data for the water graph."""
        response = make_response(json.dumps(self.water_repository.fetch_all()))
        response.headers['Content-Type'] = 'application/json'
        return response

    def handle_storm_request(self):
        """Host JSON graph data for the wind graph."""
        return jsonify(
            self.storm_repository.fetch_graph_data()
        )

    def handle_dbfetch_request(self):
        """If the request method is POST decode status data and send back."""
        if request.method == 'POST':
            storm_data = request.data.decode('utf-8')
            json_encode = json.loads(storm_data)

            for status in json_encode:
                global statuses
                statuses = json_encode[status]

            return jsonify({
                'data_transfer': statuses,
                'status': 'succeed'
            })
