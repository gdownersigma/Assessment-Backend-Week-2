"""An API for handling marine experiments."""

from datetime import datetime

from flask import Flask, jsonify, request
from psycopg2 import sql

from database_functions import get_db_connection, get_all_experiments


app = Flask(__name__)


def validate_type(type: str) -> bool:
    '''Return if type query is valid.'''
    return type in {'intelligence', 'obedience', 'aggression'}


def validate_score_over(threshold: str) -> int:
    '''Return if threshold query is valid.'''
    return threshold in range(0, 101)


"""
For testing reasons; please ALWAYS use this connection. 

- Do not make another connection in your code
- Do not close this connection

If you do not understand this instructions; as a coach to explain
"""
conn = get_db_connection("marine_experiments")


@app.get("/")
def home():
    """Returns an informational message."""
    return jsonify({
        "designation": "Project Armada",
        "resource": "JSON-based API",
        "status": "Classified"
    })


@app.route("/experiment", methods=['GET'])
def experiment():
    """API endpoint for accessing experiment."""
    if request.args.get('type', False):

    result = get_all_experiments(conn)
    return result, 200


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
