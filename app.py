import os
import time

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def database_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", "5432")),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=3,
    )


@app.get("/")
def index():
    return jsonify({"service": "elevvo-task5", "status": "ok"})


@app.get("/db-time")
def db_time():
    last_error = None
    for _ in range(10):
        try:
            with database_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT CURRENT_TIMESTAMP")
                    current_time = cursor.fetchone()[0]
            return jsonify({"database_time": current_time.isoformat()})
        except psycopg2.OperationalError as error:
            last_error = error
            time.sleep(1)

    app.logger.error("Database connection failed: %s", last_error)
    return jsonify({"error": "database unavailable"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
