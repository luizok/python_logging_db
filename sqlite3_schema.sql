CREATE TABLE IF NOT EXISTS error_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time DATETIME,
    level VARCHAR(10),
    path VARCHAR(512),
    lineno INTEGER,
    message MEDIUMTEXT -- up to 16MB
);