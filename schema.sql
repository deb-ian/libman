BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"salt"	TEXT NOT NULL,
	"password_hash"	TEXT NOT NULL,
	PRIMARY KEY("user_id")
);
CREATE TABLE IF NOT EXISTS "book_type" (
	"isbn"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"author"	TEXT NOT NULL,
	"genre"	TEXT NOT NULL,
	"date_pubished"	TEXT NOT NULL,
	"latest_revision"	TEXT NOT NULL,
	PRIMARY KEY("isbn")
);
CREATE TABLE IF NOT EXISTS "books" (
	"book_id"	INTEGER NOT NULL UNIQUE,
	"isbn"	INTEGER NOT NULL,
	"condition"	TEXT NOT NULL,
	"borrower_id"	INTEGER,
	PRIMARY KEY("book_id"),
	FOREIGN KEY("borrower_id") REFERENCES "members"("member_id"),
	FOREIGN KEY("isbn") REFERENCES "book_type"("isbn")
);
CREATE TABLE IF NOT EXISTS "members" (
	"member_id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"phone_number"	TEXT NOT NULL,
	"member_since"	INTEGER NOT NULL,
	PRIMARY KEY("member_id")
);
COMMIT;
