from flask import Flask, jsonify, request
import os
import sys
import pandas as pd
from tabulate import tabulate
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from IPython.display import display, Markdown


config_map = {
    'user':'CMSC508_USER',
    'password':'CMSC508_PASSWORD',
    'host':'CMSC508_HOST',
    'database':'FLASK_DB_NAME'
}
# load and store credentials
load_dotenv()
config = {}
for key in config_map.keys():
    config[key] = os.getenv(config_map[key])
flag = False
for param in config.keys():
    if config[param] is None:
        flag = True
        print(f"Missing {config_map[param]} in .env file")

# build a sqlalchemy engine string
engine_uri = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['database']}"


# create a database connection.  THIS IS THE ACTUAL CONNECTION!
try:
    conn = create_engine(engine_uri)
except ArgumentError as e:
    print(f"create_engine: Argument Error: {e}")
    #sys.exit(1)
except NoSuchModuleError as e:
    print(f"create_engine: No Such Module Error: {e}")
    #sys.exit(1)
except Exception as e:
    print(f"create_engine: An error occurred: {e}")
    #sys.exit(1)


## This is a helper function to keep the QMD file looking cleaner!

def my_sql_wrapper( query ):
    """ takes a query and returns a pandas dataframe for output """
    try:
        df = pd.read_sql( query, conn )
    except Exception as e:
        df = pd.DataFrame({'Query error': ["(see error message above)"]})
        msg = str(e).replace(") (",")\n(")
        print(msg)
    return df

def my_sql_statement( statement ):
    """ used with DDL, when the statement doesn't return any results. """
    try:
        with conn.begin() as x:
            x.execute(text(statement))
            x.commit()
    #    conn = create_engine(engine_uri)
        result = ""
    except Exception as e:
        result = f"Error: {str(e)}"
#    conn = create_engine(engine_uri)
    return result



#create flask web application
app = Flask(__name__)

#assinging keys
app.config['SECRET_KEY'] = 'LET_ME_IN_LET_ME_IN'

#function to check the header for auth token
@app.before_request
def check_token():
    token = request.headers.get('Authorization')
    if token != 'Bearer ' + app.config['SECRET_KEY']:
        return jsonify(message='Access Denied! Invalid Token.'), 401


# define a route and view function

@app.route('/api/tables')
def hello_table():
    df = my_sql_wrapper("show tables")
    json_data = df.to_json()
    return json_data

@app.route('/api/tables/player')
def get_players():
    df = my_sql_wrapper("select * from player")
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/api/tables/locations')
def get_locations():
    df = my_sql_wrapper("select * from locations")
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/api/tables/NPC')
def get_NPC():
    df = my_sql_wrapper("select * from NPC")
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/api/tables/item')
def get_item():
    df = my_sql_wrapper("select * from item")
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/api/tables/game')
def get_game():
    df = my_sql_wrapper("select * from game")
    json_data = df.to_json(orient='records')
    return json_data

## Getting a single object data for each table
@app.route('/api/tables/player/<int:player_id>')
def get_one_players(player_id):
    df = my_sql_wrapper("select * from player where player_id = " + str(player_id))
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/api/tables/locations/<int:location_id>')
def get_one_location(location_id):
    df = my_sql_wrapper("select * from locations where location_id = " + str(location_id))
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/api/tables/NPC/<int:NPC_id>')
def get_one_NPC(NPC_id):
    df = my_sql_wrapper("select * from NPC where NPC_id = " + str(NPC_id))
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/api/tables/game/<int:game_id>')
def get_one_game(game_id):
    df = my_sql_wrapper("select * from game where game_id = " + str(game_id))
    json_data = df.to_json(orient='records')
    return json_data

@app.route('/api/tables/item/<int:item_id>')
def get_one_item(item_id):
    df = my_sql_wrapper("select * from item where item_id = " + str(item_id))
    json_data = df.to_json(orient='records')
    return json_data




# run the application
if __name__ == '__main__':
    app.run()
