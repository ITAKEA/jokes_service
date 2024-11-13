from flask import Flask, jsonify
import random
from jokes_data import jokes
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Service information and available endpoints',
            'schema': {
                'type': 'object',
                'properties': {
                    'service': {'type': 'string'},
                    'version': {'type': 'string'},
                    'description': {'type': 'string'},
                    'documentation': {'type': 'string'},
                    'health': {'type': 'string'}
                }
            }
        }
    }
})
def root():
    return jsonify({
        "service": "Joke Service",
        "version": "1.0.0",
        "description": "A RESTful API service that provides jokes",
        "documentation": "/api",
        "health": "/health"
    })

@app.route('/api', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'API documentation with all available endpoints',
            'schema': {
                'type': 'object',
                'properties': {
                    'endpoints': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'path': {'type': 'string'},
                                'method': {'type': 'string'},
                                'description': {'type': 'string'},
                                'response': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def api_documentation():
    return jsonify({
        "endpoints": [
            {
                "path": "/",
                "method": "GET",
                "description": "Service information and available endpoints",
                "response": "JSON object with service details"
            },
            {
                "path": "/api",
                "method": "GET",
                "description": "API documentation with all available endpoints",
                "response": "JSON object with endpoint details"
            },
            {
                "path": "/api/jokes",
                "method": "GET",
                "description": "Get all available jokes",
                "response": "Array of joke objects"
            },
            {
                "path": "/api/jokes/random",
                "method": "GET",
                "description": "Get a random joke",
                "response": "Single joke object"
            },
            {
                "path": "/api/jokes/<id>",
                "method": "GET",
                "description": "Get a specific joke by ID",
                "response": "Single joke object or 404 error"
            },
            {
                "path": "/health",
                "method": "GET",
                "description": "Health check endpoint",
                "response": "JSON object with service health status"
            }
        ]
    })

@app.route('/api/jokes', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all jokes',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'setup': {'type': 'string'},
                        'punchline': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_all_jokes():
    return jsonify(jokes)

@app.route('/api/jokes/random', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A random joke',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'setup': {'type': 'string'},
                    'punchline': {'type': 'string'}
                }
            }
        }
    }
})
def get_random_joke():
    return jsonify(random.choice(jokes))

@app.route('/api/jokes/<int:joke_id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'joke_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the joke to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'The requested joke',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'setup': {'type': 'string'},
                    'punchline': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Joke not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def get_joke_by_id(joke_id):
    joke = next((joke for joke in jokes if joke['id'] == joke_id), None)
    if joke is None:
        return jsonify({"error": "Joke not found"}), 404
    return jsonify(joke)

@app.route('/health', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Health check status',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'}
                }
            }
        }
    }
})
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run()
