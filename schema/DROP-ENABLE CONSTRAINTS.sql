-- Disable foreign key constraints
ALTER TABLE tickets DISABLE TRIGGER ALL;

ALTER TABLE categories DROP CONSTRAINT fk_category;
ALTER TABLE departments DROP CONSTRAINT fk_deparment;
ALTER TABLE urgency DROP CONSTRAINT fk_urgency;

TRUNCATE TABLE categories, departments, urgency, tickets;

-- Re-enable foreign key constraints
ALTER TABLE tickets ENABLE TRIGGER ALL;

ALTER TABLE categories ADD CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES categories(category_id);
ALTER TABLE departments ADD CONSTRAINT fk_deparment FOREIGN KEY (dept_id) REFERENCES departments(dept_id);
ALTER TABLE urgency ADD CONSTRAINT fk_urgency FOREIGN KEY (urgency_id) REFERENCES urgency(urgency_id);
