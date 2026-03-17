import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
from psycopg import sql

from app.models.metrics import Metric

@contextmanager
def get_db():
    conn = psycopg.connect(
        "dbname=iot_data user=postgres password=root",
    )
    try:
        yield conn
    finally:
        conn.close()

def insert_sensor_data(device_id, temperature, humidity, lux):

    with get_db() as conn:    
        with conn.cursor() as cur: 

            cur.execute(
                """
                INSERT INTO sensor_data (device_id, temperature, humidity, lux)
                VALUES (%s, %s, %s, %s)
                """,
                (device_id, temperature, humidity, lux)
            )

        conn.commit()

def get_latest_data():
        
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                """
                    SELECT *
                    FROM sensor_data
                    ORDER BY time DESC
                    LIMIT 25
                """
            )

            return cur.fetchall()

VALID_METRICS = {"temperature", "humidity", "lux"}

def get_average_data(metric: Metric):

    metric_name = metric.value

    if metric_name not in VALID_METRICS:
        raise ValueError("Métrica inválida")

    query = sql.SQL(
        """
        SELECT
            time_bucket('10 minutes', time) AS bucket,
            AVG({metric}) AS avg
        FROM sensor_data
        GROUP BY 1
        ORDER BY 1
        """
    ).format(metric=sql.Identifier(metric))

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query)
            return cur.fetchall()
