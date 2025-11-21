"""Functions that interact with the database."""
from datetime import datetime
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def get_db_connection(dbname,
                      password="postgres") -> connection:
    """Returns a DB connection."""

    return connect(dbname=dbname,
                   host="localhost",
                   port=5432,
                   password=password,
                   cursor_factory=RealDictCursor)


# pylint: disable=line-too-long, dangerous-default-value
def get_all_experiments(conn: connection, threshold: int = 0, types: list = ['intelligence', 'obedience', 'aggression']) -> list[dict]:
    """Return a list of all the experiments as dictionaries."""
    cur = conn.cursor()
    cur.execute("""SELECT experiment_id,
       subject_id,
       species_name AS species,
       experiment_date,
       type_name AS experiment_type,
       ROUND(((score/max_score)*100)::NUMERIC,2)AS score
    FROM experiment
    JOIN subject
        USING (subject_id)
    JOIN experiment_type
        USING (experiment_type_id)
    JOIN species
        USING (species_id) 
    WHERE ROUND(((score/max_score)*100)::NUMERIC,2) > %s 
    AND type_name = ANY(%s)
    ORDER BY experiment_date DESC;""", (threshold, types))
    results = cur.fetchall()
    for result in results:
        result['experiment_date'] = datetime.strftime(
            result['experiment_date'], '%Y-%m-%d')
        result['score'] = str(result['score'])
    cur.close()
    return results


def delete_experiment_from_id(conn: connection, experiment_id: int) -> dict:
    """Deletes an experiment from the database."""
    cur = conn.cursor()
    cur.execute(
        """DELETE FROM experiment WHERE experiment_id = %s RETURNING *""", (experiment_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    if deleted:
        deleted['experiment_date'] = datetime.strftime(
            deleted['experiment_date'], '%Y-%m-%d')
    return deleted


if __name__ == '__main__':
    connection_2 = get_db_connection('marine_experiments')
    get_all_experiments(connection_2)
    connection_2.close()
