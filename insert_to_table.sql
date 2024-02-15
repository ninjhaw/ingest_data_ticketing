-- Insert into categories table
INSERT INTO categories (category_name)
SELECT DISTINCT "category_name" FROM tickets_temp;

-- Insert into departments table
INSERT INTO departments (dept_name)
SELECT DISTINCT "department_name" FROM tickets_temp;

-- Insert into urgency table
INSERT INTO urgency (urgency_name)
SELECT DISTINCT "Urgency" FROM tickets_temp;

-- Insert into tickets table with foreign key references
INSERT INTO tickets (ticket_id, created_date, status, subject, resolve_date, remarks, category_id, dept_id, urgency_id)
SELECT
    "ticket_id",
    "created_date",
    "Status" as "status",
    "Subject" as "subject",
    "resolved_date",
    "remarks",
    c.category_id,
    d.dept_id,
    u.urgency_id
FROM tickets_temp t
LEFT JOIN categories c ON t."category_name" = c.category_name
LEFT JOIN departments d ON t."department_name" = d.dept_name
LEFT JOIN urgency u ON t."Urgency" = u.urgency_name;
