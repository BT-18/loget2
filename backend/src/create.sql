USE Syslog;

CREATE TABLE IF NOT EXISTS Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(50) UNIQUE NOT NULL,
    hash VARCHAR(255) NOT NULL,
    role VARCHAR(50),
    totp VARCHAR(255),
    CONSTRAINT validRole CHECK(
        role IN ('user','admin')
    )
);

CREATE TABLE IF NOT EXISTS Groups(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS UserGroup(
    user_id INT,
    group_id INT,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES Groups(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Entities(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS EntityGroup(
    entity_id INT,
    group_id INT,
    PRIMARY KEY (entity_id, group_id),
    FOREIGN KEY (entity_id) REFERENCES Entity(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES Groups(id) ON DELETE CASCADE
);


# Création Index pour améliorer la vitesse des requêtes (pour supprimer: ALTER TABLE SystemEvents DROP INDEX nom_index)
CREATE FULLTEXT INDEX idx_message_fulltext ON SystemEvents(Message);
CREATE INDEX idx_devicereportedtime ON SystemEvents(DeviceReportedTime);
CREATE INDEX idx_fromhost_time ON SystemEvents(FromHost, DeviceReportedTime);
CREATE INDEX idx_fromhost ON SystemEvents(FromHost);
CREATE INDEX idx_receivedat ON SystemEvents(ReceivedAt);
CREATE INDEX idx_fromhost_receivedat ON SystemEvents(FromHost, ReceivedAt DESC);

INSERT INTO Users (email, hash, role) VALUES ('admin@test.com', "1234", 'admin')
INSERT INTO Users (email, hash, role) VALUES ('user@test.com', "1234", 'user')
