from flask import Flask, render_template
import json
from settings import *


app = Flask( __name__ )

database = connect( DATABASE, check_same_thread=False )

@app.route( "/data" )
def data():

    values = database.execute( """
        SELECT PH, EC, TEMP_DRY, HUMIDITY_DRY, TEMP_WET, FAN_DRY, FAN_WET, FOGGER
        FROM krydderino
        WHERE timestamp=( SELECT MAX(timestamp) FROM krydderino )
    """ ).fetchone()

    return json.dumps( dict( zip( FIELDS, values ) ) )

@app.route( "/" )
def index():
    return render_template( 'main.html' )

if __name__ == "__main__":
    app.run( debug=True )



