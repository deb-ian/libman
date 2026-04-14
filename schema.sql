BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "book_type" (
	"isbn"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"author"	TEXT NOT NULL,
	"genre"	TEXT NOT NULL,
	"date_published"	TEXT NOT NULL,
	"latest_revision"	TEXT NOT NULL,
	PRIMARY KEY("isbn")
);
CREATE TABLE IF NOT EXISTS "books" (
	"book_id"	INTEGER NOT NULL UNIQUE,
	"isbn"	INTEGER NOT NULL,
	"condition"	TEXT NOT NULL,
	PRIMARY KEY("book_id"),
	FOREIGN KEY("isbn") REFERENCES "book_type"("isbn")
);
CREATE TABLE IF NOT EXISTS "borrowhistory" (
	"borrow_id"	INTEGER NOT NULL UNIQUE,
	"book_id"	INTEGER NOT NULL,
	"member_id"	INTEGER NOT NULL,
	"issued_at"	TEXT NOT NULL,
	"issuer_id"	INTEGER NOT NULL,
	"due_by"	TEXT NOT NULL,
	PRIMARY KEY("borrow_id"),
	FOREIGN KEY("book_id") REFERENCES "books"("book_id"),
	FOREIGN KEY("issuer_id") REFERENCES "superuser"("user_id"),
	FOREIGN KEY("member_id") REFERENCES "members"("member_id")
);
CREATE TABLE IF NOT EXISTS "members" (
	"member_id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"phone_number"	TEXT NOT NULL,
	"member_since"	INTEGER NOT NULL,
	PRIMARY KEY("member_id")
);
CREATE TABLE IF NOT EXISTS "superuser" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"salt"	TEXT NOT NULL,
	"password_hash"	TEXT NOT NULL,
	"role"	TEXT NOT NULL DEFAULT 'HELPER', --Possible values 'HELPER', 'ADMIN', 'LIBRARIAN'
	PRIMARY KEY("user_id")
);
COMMIT;
