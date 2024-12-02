from flask import Flask, jsonify, request
from pymongo import MongoClient
import psycopg2
from py2neo import Graph

app = Flask(__name__)

# MongoDB connection
mongo_client = MongoClient("mongo_db", 27017)
mongo_db = mongo_client["iot"]

# PostgreSQL connection
pg_connection = psycopg2.connect(
    host="sql_db",
    port=5432,
    database="iot_data",
    user="postgres",
    password="password"
)

# Neo4j connection
neo4j_graph = Graph("bolt://neo4j_db:7687", auth=("neo4j", "password"))


@app.route("/api/mongo", methods=["GET"])
def get_mongo_data():
    data = list(mongo_db["sensor_data"].find({}, {"_id": 0}))
    return jsonify(data)


@app.route("/api/postgres", methods=["GET"])
def get_postgres_data():
    with pg_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sensor_data;")
        data = cursor.fetchall()
    return jsonify(data)


@app.route("/api/neo4j", methods=["GET"])
def get_neo4j_data():
    query = "MATCH (n) RETURN n LIMIT 25"
    data = [{"node": dict(record["n"])} for record in neo4j_graph.run(query)]
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
