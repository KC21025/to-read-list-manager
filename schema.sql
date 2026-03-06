DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Status;

/*
-- SQL schema for a book tracking application
-- Created Author table, and added the ID, name
*/

CREATE TABLE Author (
    Author_ID INTEGER PRIMARY KEY,
    Author_Name TEXT
);

/*
-- Created Status table, ID and name.
*/

CREATE TABLE Status (
    Status_ID INTEGER PRIMARY KEY,
    Status_Name TEXT
);

/*
-- Created Item table, added FKs to Author and Status and other relevant things for a book item
*/

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

/*
-- Inserted some default status values for the Status table
*/

INSERT INTO Status (Status_ID, Status_Name) Values (1, 'Reading');
INSERT INTO Status (Status_ID, Status_Name) Values (2, 'Completed');
INSERT INTO Status (Status_ID, Status_Name) Values (3, 'To Read');