CREATE TABLE IF NOT EXISTS Collabs_Join
(
    Collaboration_ID INTEGER,
    Collaborator_ID INTEGER,
    FOREIGN KEY (Collaboration_ID) REFERENCES Collaborations(Collaboration_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (Collaborator_ID) REFERENCES Collaborators(Collaborator_ID)
)