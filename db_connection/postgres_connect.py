from sqlalchemy import create_engine
import psycopg2, json

def get_postgres_credentials(path='config.json'):
    with open(path, 'r') as file:
        config = json.load(file)
    return config['postgres']

# connect to postgres using create_engine
# def connect_to_postgres():
#     credentials = get_postgres_credentials()
#     connection_string = (
#         f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['database']}"
#     )
#     engine = create_engine(connection_string)
#     connection = engine.connect()
#     return connection