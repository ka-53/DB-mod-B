import paho.mqtt.client as mqtt
from pymongo import MongoClient
from py2neo import Graph, Node
import psycopg2

# MongoDB setup
mongo_client = MongoClient("mongo_db", 27017)
mongo_db = mongo_client["iot_database"]
mongo_collection = mongo_db["sensor_data"]

# PostgreSQL setup
pg_conn = psycopg2.connect(
    dbname="iot_data",
    user="postgres",
    password="password",
    host="sql_db",
)
pg_cursor = pg_conn.cursor()

# Neo4j setup
neo4j_graph = Graph("bolt://neo4j_db:7687", auth=("neo4j", "password"))

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with code:", rc)
    client.subscribe("iot/data/#")

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")
    # Example routing logic
    if msg.topic == "iot/data/mongo":
        mongo_collection.insert_one({"message": msg.payload.decode()})
    elif msg.topic == "iot/data/sql":
        pg_cursor.execute(
            "INSERT INTO sensor_data (sensor_id, value, timestamp) VALUES (%s, %s, %s)",
            ("sensor_1", 25.5, "2024-12-01 12:00:00"),
        )
        pg_conn.commit()
    elif msg.topic == "iot/data/neo4j":
        node = Node("Sensor", name="sensor_1", value=25.5)
        neo4j_graph.create(node)

# MQTT Client setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("mqtt_server", 1883, 60)
mqtt_client.loop_forever()
