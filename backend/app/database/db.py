import psycopg
from psycopg import sql as pgsql
from psycopg.rows import dict_row
from contextlib import contextmanager
from psycopg import sql

from datetime import datetime
from typing import Optional

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

def get_latest_data(from_time: Optional[datetime] = None, to_time: Optional[datetime] = None):
    
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
    
            query = """
                SELECT *
                FROM sensor_data
            """
            filters, params = [], []

            if from_time is not None:
                filters.append("time >= %s")
                params.append(from_time)
            if to_time is not None:
                filters.append("time <= %s")
                params.append(to_time)

            if filters:
                query += " WHERE " + " AND ".join(filters)

            query += " ORDER BY time DESC"

            # converte para o tipo que psycopg espera (QueryNoTemplate)
            cur.execute(pgsql.SQL(query), tuple(params))

            return cur.fetchall()

VALID_METRICS = {"temperature", "humidity", "lux"}

def get_average_data(metric: Metric):

    if metric.value not in VALID_METRICS:
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
