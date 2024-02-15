from sqlalchemy import create_engine
import pandas as pd

# create connection to postgres
engine = create_engine(f'postgresql://postgres:netlab123@172.19.30.77:5432/ticketing')

# read the csv file
df = pd.read_csv('Datasets/tickets.csv')

# Dropping column category
df.drop(columns=['Category'], inplace=True)

# renaming the column headers
df.rename(columns={"Created Date":"created_date", "Ticket No.": "ticket_id","Sub-Category": "category_name", "Isolation": "remarks", "Date Resolved": "resolved_date", "Department": "department_name"}, inplace=True)

# Strip the characters `#INC-`
df['ticket_id'] = df['ticket_id'].str.strip('#INC-')

# convert data types according to the column and also data
df['ticket_id'] = df['ticket_id'].astype('int')
df['created_date'] = pd.to_datetime(df['created_date'])
df['resolved_date'] = pd.to_datetime(df['resolved_date'])

df.head(n=0).to_sql(name="tickets_temp")
df.to_sql(name="tickets_temp", con=engine, if_exists="replace", index=False)





