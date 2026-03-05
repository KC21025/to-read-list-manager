CREATE TABLE Author (
    Author_ID INTEGER PRIMARY KEY,
    Author_Name TEXT
);

CREATE TABLE Status (
    Status_ID INTEGER PRIMARY KEY,
    Status_Name TEXT
);

CREATE TABLE Item (
    Item_ID INTEGER PRIMARY KEY,
    Author_ID INTEGER,
    Status_ID INTEGER,
    Title TEXT,
    Total_Pages INTEGER,
    Pages_Read INTEGER,
    Date_Started DATE,
    Date_Finished DATE,
    Rating NUMBER,
    FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID),
    FOREIGN KEY (Status_ID) REFERENCES Status(Status_ID)
);

INSERT INTO Status (Status_ID, Status_Name) Values (1, 'Reading'),
INSERT INTO Status (Status_ID, Status_Name) Values (2, 'Completed')
INSERT INTO Status (Status_ID, Status_Name) Values (3, 'To Read'),