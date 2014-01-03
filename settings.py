from sqlite3 import *

FIELDS = (
    "PH",
    "EC",
    "TEMP_DRY",
    "HUMIDITY_DRY",
    "TEMP_WET",
    "FAN_DRY",
    "FAN_WET",
    "FOGGER"
)

DATABASE = 'db/krydderino.db'

SERIAL_BAUDRATE = 9600

SERIAL_PORT = '/dev/tty.usbmodem1411'


database = connect( DATABASE, check_same_thread=False )