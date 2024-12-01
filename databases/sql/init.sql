CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50),
    value FLOAT,
    timestamp TIMESTAMP
);
