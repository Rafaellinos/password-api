CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL NOT NULL,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
);

CREATE TABLE password (
	id INTEGER NOT NULL,
	password VARCHAR,
	password_requests_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(password_requests_id) REFERENCES password_requests (id)
);

CREATE TABLE password_requests (
	id INTEGER NOT NULL,
	create_date DATETIME,
	user_id INTEGER,
	due_date DATETIME,
	view_counter INTEGER,
	status VARCHAR(8),
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES users (id),
	CONSTRAINT passwordrequestsstatus CHECK (status IN ('new', 'valid', 'canceled'))
);

INSERT INTO users (username,password)
VALUES ('admin', 'admin', );
