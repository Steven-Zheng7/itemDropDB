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

## Getting all item type
@app.route('/api/tables/item/')
def get_filter_item():
    item_type = request.args.get('type')
    item_source = request.args.get('item_source')
    if item_type:
        df = my_sql_wrapper("select * from item where item_type = " + "\"" + str(item_type) + "\"")
        json_data = df.to_json(orient='records')
    elif item_source:
        item_source = item_source.replace('+', ' ')
        df = my_sql_wrapper("select item_name, NPC_name, location_name, game_name from item a inner join NPC b on (a.item_id=b.item_id) inner join located c on (b.NPC_id=c.NPC_id) inner join locations d on (c.location_id=d.location_id) inner join game e on (e.game_id=d.game_id) where a.item_name = " + "\"" + str(item_source) + "\"")
        json_data = df.to_json(orient='records')
    return json_data
## Insert into db Endpoint
# item_id, item_name, item_type, item_def, item_atk, item_recipe, item_effect
@app.route('/api/tables/item/add/')
def add_item():
    id = request.args.get('item_id')
    name = request.args.get('item_name')
    type = request.args.get('item_type')
    deff = request.args.get('item_def')
    atk = request.args.get('item_atk')
    recipe = request.args.get('item_recipe')
    effect = request.args.get('item_effect')

    if any(param is None or not param.strip() for param in [id, name, type, deff, atk, recipe, effect]):
        return jsonify({'Error': 'You did not provide the correct parameters.'}), 404
    else:
        id = int(id)
        deff = int(deff)
        atk = int(atk)
        
        name = name.replace('+', ' ')
        type = type.replace('+', ' ')
        recipe = recipe.replace('+', ' ')
        effect = effect.replace('+', ' ')
        my_sql_statement(f"insert into item(item_id, item_name, item_type, item_def, item_atk, item_recipe, item_effect) values ({id}, '{name}', '{type}', {deff}, {atk}, '{recipe}', '{effect}');")
        return jsonify({'New Data Added': 'Successful'}), 200
    
# Delete endpoint in the item table 
@app.route('/api/tables/item/delete/')
def delete_item():
    id = request.args.get('item_id')

    if any(param is None or not param.strip() for param in [id]):
        return jsonify({'Error': 'You did not provide the correct parameters.'}), 404
    else:
        id = int(id)
        
        my_sql_statement(f"delete from item where item_id={id};")
        return jsonify({'Data Deleted': 'Successful'}), 200
    
# Update endpoint in item table 
@app.route('/api/tables/item/update/')
def update_item():
    id = request.args.get('item_id')
    name = request.args.get('item_name')
    type = request.args.get('item_type')
    deff = request.args.get('item_def')
    atk = request.args.get('item_atk')
    recipe = request.args.get('item_recipe')
    effect = request.args.get('item_effect')

    if any(param is None or not param.strip() for param in [id, name, type, deff, atk, recipe, effect]):
        return jsonify({'Error': 'You did not provide the correct parameters.'}), 404
    else:
        id = int(id)
        deff = int(deff)
        atk = int(atk)
        
        name = name.replace('+', ' ')
        type = type.replace('+', ' ')
        recipe = recipe.replace('+', ' ')
        effect = effect.replace('+', ' ')
        my_sql_statement(f"update item set item_id={id}, item_name='{name}', item_type='{type}', item_def={deff}, item_atk={atk}, item_recipe='{recipe}', item_effect='{effect}' where item_id={id};")
        return jsonify({'Data updated': 'Successful'}), 200
    
# run the application
if __name__ == '__main__':
    app.run()
