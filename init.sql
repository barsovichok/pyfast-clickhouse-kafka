CREATE DATABASE IF NOT EXISTS default;

CREATE TABLE IF NOT EXISTS default.events (
    event_type String,
    description String,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY timestamp;