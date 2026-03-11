/*
-- Drops tables if they already exist to avoid errors when running the database setup multiple times
*/

DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Status;

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
    Total_Pages INTEGER NOT NULL Check (typeof(Total_Pages) = 'integer'),
    Pages_Read INTEGER Check (Pages_Read >= 0 and Pages_Read <= Total_Pages),
    Date_Started DATE,
    Date_Finished DATE,
    Rating NUMBER Check (Rating >= 0 and Rating <= 5),
    FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID),
    FOREIGN KEY (Status_ID) REFERENCES Status(Status_ID)
);

/*
-- Inserted some default status values for the Status table
*/

INSERT INTO Status (Status_ID, Status_Name) Values (1, 'Reading');
INSERT INTO Status (Status_ID, Status_Name) Values (2, 'Completed');
INSERT INTO Status (Status_ID, Status_Name) Values (3, 'To Read');

INSERT INTO Author (Author_ID, Author_Name) Values (1, 'J.K. Rowling');

INSERT INTO Item (Item_ID, Author_ID, Status_ID, Title, Total_Pages, Pages_Read, Date_Started, Date_Finished, Rating) Values (1, 1, 3, 'Harry Potter and the Sorcerer''s Stone', 309, 309, '2024-01-01', '2024-01-15', 5);