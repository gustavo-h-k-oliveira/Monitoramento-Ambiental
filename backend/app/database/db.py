import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager

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

def get_average_temp():

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                """
                    SELECT
                        time_bucket('10 minutes', time),
                        AVG(temperature)
                    FROM sensor_data
                    GROUP BY 1
                    ORDER BY 1
                """
            )

            return cur.fetchall()
