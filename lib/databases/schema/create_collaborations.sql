CREATE TABLE IF NOT EXISTS Collaborations
(
    Collaboration_ID SERIAL PRIMARY KEY NOT NULL,
    Name TEXT UNIQUE NOT NULL,
    Description TEXT UNIQUE NOT NULL,
    Content TEXT
)