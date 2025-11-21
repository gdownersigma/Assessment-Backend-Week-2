# pylint: disable=pointless-string-statement, too-many-return-statements

"""An API for handling marine experiments."""
from flask import Flask, jsonify, request

from database_functions import get_db_connection, get_all_experiments, delete_experiment_from_id


app = Flask(__name__)


def validate_type(exp_type: str) -> bool:
    '''Return if type query is valid.'''
    return exp_type.lower() in {'intelligence', 'obedience', 'aggression'}


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
    exp_type = request.args.get('type', False)
    score_over = request.args.get('score_over', False)

    if exp_type and score_over:
        if not validate_type(exp_type):
            return {
                'error': "Invalid value for 'type' parameter",
            }, 400
        try:
            if not validate_score_over(int(score_over)):
                return {
                    'error': "Invalid value for 'score_over' parameter"
                }, 400
        except ValueError:
            return {
                'error': "Invalid value for 'score_over' parameter"
            }, 400
        result = get_all_experiments(conn, score_over, [exp_type.lower()])
    elif exp_type:
        if not validate_type(exp_type):
            return {
                'error': "Invalid value for 'type' parameter",
            }, 400
        result = get_all_experiments(conn, types=[exp_type.lower()])
    elif score_over:
        try:
            if not validate_score_over(int(score_over)):
                return {
                    'error': "Invalid value for 'score_over' parameter"
                }, 400
        except ValueError:
            return {
                'error': "Invalid value for 'score_over' parameter"
            }, 400
        result = get_all_experiments(conn, score_over)
    else:
        result = get_all_experiments(conn)

    return result, 200


@app.delete("/experiment/<int:experiment_id>")
def delete_experiment(experiment_id: int):
    """Deletes an experiment from the given ID."""
    result = delete_experiment_from_id(conn, experiment_id)
    if result is None:
        return {
            "error": f"Unable to locate experiment with ID {experiment_id}."
        }, 404
    return result


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
