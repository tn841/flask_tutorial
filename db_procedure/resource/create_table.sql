CREATE TABLE BOOKS(
	bookID CHAR(5) NOT NULL,
    bookNme varchar(50) NOT NULL,
    bookOriginPrice Double not null,
    bookType varchar(10) not null,
	primary key(bookID)
);

CREATE TABLE BOOKS_SELL(
	bookID CHAR(5) NOT NULL,
    bookSellPrice DOUBLE NOT NULL,
    bookType VARCHAR(5) NOT NULL,
	primary key(bookID)
);