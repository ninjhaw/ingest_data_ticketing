from sqlalchemy import create_engine
from time import time
import pandas as pd
import numpy as np
import psycopg2
from db_connection import postgres_connect as pc

db = pc.get_postgres_credentials()
conn = psycopg2.connect(
    host=db['host'],
    database=db['database'],
    user=db['user'],
    password=db['password'],
    port=db['port'])

engine = create_engine(f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}")
try:
    # read the csv file
    df = pd.read_csv('datasets/Tickets.csv')

    # Dropping column category
    df.drop(columns=['Category'], inplace=True)

    # renaming the column headers
    df.rename(columns={"Created Date":"created_date", "Ticket No.": "ticket_id","Sub-Category": "category_name", "Isolation": "remarks", "Date Resolved": "resolved_date", "Department": "department_name"}, inplace=True)

    # Strip the characters `#INC-`
    df['ticket_id'] = df['ticket_id'].str.strip('#INC-')

    # impute null values in urgency and department columns
    df['Urgency'] = df['Urgency'].apply(lambda x: np.random.choice(['Urgent', 'High', 'Medium', 'Low']) if pd.isnull(x) else x)
    unique_dept = df['department_name'].dropna().unique()
    df['department_name'] = df['department_name'].fillna(pd.Series(np.random.choice(unique_dept, size=len(df.index))))


    # convert data types according to the column and also data
    df['ticket_id'] = df['ticket_id'].astype('int')
    df['created_date'] = pd.to_datetime(df['created_date'])
    df['resolved_date'] = pd.to_datetime(df['resolved_date'])

    # drop any duplicates
    df.drop_duplicates()

    # upload the header of the table
    df.head(n=0).to_sql(name="tickets_temp", con=engine, if_exists="replace", index=False)
    # insert data into database
    df.to_sql(name="tickets_temp", con=engine, if_exists="replace", index=False)


    # This is for inserting data into separate tables
    try:
        with conn.cursor() as cursor:
            # Insert into categories table
            cursor.execute("""
                -- Insert into categories table
                INSERT INTO categories (category_name)
                SELECT DISTINCT "category_name" FROM tickets_temp
                WHERE "category_name" NOT IN (SELECT category_name FROM categories);

                -- Insert into departments table
                INSERT INTO departments (dept_name)
                SELECT DISTINCT "department_name" FROM tickets_temp
                WHERE "department_name" NOT IN (SELECT dept_name FROM departments);

                -- Insert into urgency table
                INSERT INTO urgency (urgency_name)
                SELECT DISTINCT "Urgency" FROM tickets_temp
                WHERE "Urgency" NOT IN (SELECT urgency_name FROM urgency);

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
                LEFT JOIN urgency u ON t."Urgency" = u.urgency_name
                ON CONFLICT (ticket_id) DO NOTHING;""")

                    # Commit the changes
        conn.commit()
    except psycopg2.errors.UniqueViolation as e:
        print(f"Skipping duplicate ticket_id: {e}")

    print("Successfully Loaded into PostgreSQL DB!")
    
    
except pd.errors.EmptyDataError:
    # Handle the case where the CSV file is empty
    print("CSV file is empty.")
except pd.errors.ParserError:
    # Handle the case where there is an issue with parsing the CSV file
    print("Error parsing CSV file.")
except FileNotFoundError:
    # Handle the case where the file is not found
    print("File not found.")
except Exception as e:
    # Catch any other unexpected exceptions
    print(f"An unexpected error occurred: {str(e)}")