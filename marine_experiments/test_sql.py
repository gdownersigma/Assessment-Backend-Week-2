import pandas as pd
import pytest

from psycopg2.extensions import connection


def read_task_csv(task_no: int) -> pd.DataFrame:
    """Reads in the expected output CSV for a given task number."""
    task_csv = pd.read_csv(
        f'expected_outputs/task_{task_no}.csv', dtype=str)
    return task_csv


def read_sql_query_from_task_number(task_no: int) -> str:
    """Reads in a SQL query from a file."""
    with open(f'queries/task_{task_no}.sql', 'r') as file:
        query = file.read()
    return query


def make_all_columns_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Makes all columns of a dataframe string into strings. Used
    here to avoid data type mismatches when comparing query results.
    """
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df


@pytest.mark.parametrize('task_no', range(1, 5))
def test_dql_query_results(test_temp_conn: connection, task_no: int) -> None:
    """Tests the DQL query results against the expected CSV output.

    Args:
        test_temp_conn (connection): The database connection to use for the test.
        task_no (int): The task number to test.
    """
    with test_temp_conn.cursor() as cur:
        # Expected result
        task_csv = read_task_csv(task_no)

        # Actual result
        dql_query = read_sql_query_from_task_number(task_no)
        cur.execute(dql_query)
        result = pd.DataFrame(cur.fetchall())
        # Turn columns into strings to match CSV reading
        result = make_all_columns_strings(result)

        # Verify that these are equal
        assert result.equals(task_csv) == True


@pytest.mark.parametrize('task_no', range(5, 8))
def test_dml_query_results(test_temp_conn: connection, task_no: int) -> None:
    """Tests the DML query results against the expected CSV output.

    Args:
        test_temp_conn (connection): The database connection to use for the test.
        task_no (int): The task number to test.
    """
    with test_temp_conn.cursor() as cur:
        # Expected result
        task_csv = read_task_csv(task_no)

        # Run DML query first
        dml_query = read_sql_query_from_task_number(task_no)
        cur.execute(dml_query)
        test_temp_conn.commit()

        # Make the selection based on task number
        if task_no == 6:
            # Task number 6 modifies the subject table
            cur.execute('SELECT * FROM subject;')
        else:
            # Task numbers 5 and 7 modify the experiment table
            cur.execute('SELECT * FROM experiment;')
        result = pd.DataFrame(cur.fetchall())
        # Turn columns into strings to match CSV reading
        result = make_all_columns_strings(result)

        # Verify that these are equal
        assert result.equals(task_csv) == True
