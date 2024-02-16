CREATE TABLE IF NOT EXISTS categories (
	category_id SERIAL PRIMARY KEY,
	category_name varchar(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS departments (
	dept_id SERIAL PRIMARY KEY,
	dept_name varchar(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS urgency (
	urgency_id SERIAL PRIMARY KEY,
	urgency_name varchar(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
	ticket_id INT NOT NULL PRIMARY KEY,
	created_date DATE NOT NULL,
	status varchar(50),
	subject varchar(200),
	resolve_date DATE,
	remarks varchar(200),
	category_id INT,
    dept_id INT,
    urgency_id INT,
	CONSTRAINT fk_category
		FOREIGN KEY(category_id)
			REFERENCES categories(category_id),
	CONSTRAINT fk_department
		FOREIGN KEY(dept_id)
			REFERENCES departments(dept_id),
	CONSTRAINT fk_urgency
		FOREIGN KEY(urgency_id)
			REFERENCES urgency(urgency_id)	
);
