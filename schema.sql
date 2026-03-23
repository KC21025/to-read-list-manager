/*
-- Drops tables if they already exist to avoid errors when running the database setup multiple times
*/

DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Status;
DROP TABLE IF EXISTS Goals;

/*
-- SQL schema for a book tracking application
-- Created Author table, and added the ID, name
*/

CREATE TABLE Author (
    Author_ID INTEGER PRIMARY KEY,
    Author_Name TEXT NOT NULL
);

/*
-- Created Status table, ID and name.
*/

CREATE TABLE Status (
    Status_ID INTEGER PRIMARY KEY,
    Status_Name TEXT NOT NULL
);

/*
-- Created Item table, added FKs to Author and Status and other relevant things for a book item
*/

CREATE TABLE Item (
    Item_ID INTEGER PRIMARY KEY,
    Author_ID INTEGER,
    Status_ID INTEGER DEFAULT 3, -- Default to 'To Read'
    Title TEXT NOT NULL,
    Book_Description TEXT,
    Total_Pages INTEGER NOT NULL CHECK (typeof(Total_Pages) = 'integer'),
    Pages_Read INTEGER CHECK (Pages_Read >= 0 AND Pages_Read <= Total_Pages) DEFAULT 0,
    Date_Started DATE,
    Date_Finished DATE DEFAULT (NULL),
    Rating INTEGER CHECK (Rating >= 0 AND Rating <= 5) DEFAULT 0, -- Default is 0 Rating
    FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID),
    FOREIGN KEY (Status_ID) REFERENCES Status(Status_ID)
);

/*
-- Created a Goal Table
*/

CREATE TABLE Goals (
    Goal_ID INTEGER PRIMARY KEY,
    Goal_Count INTEGER NOT NULL DEFAULT 0
);

/*
-- Inserted some default status values for the Status table
*/

INSERT INTO Goals( Goal_ID, Goal_Count) Values (1, 0);
INSERT INTO Status (Status_ID, Status_Name) Values (1, 'Reading');
INSERT INTO Status (Status_ID, Status_Name) Values (2, 'Completed');
INSERT INTO Status (Status_ID, Status_Name) Values (3, 'To Read');