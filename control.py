from serial import Serial
from serial.serialutil import SerialException
from re import match, findall, split
from settings import *
from sqlite3 import *
from serial.tools import list_ports_posix


class Receiver( object ):

    def __init__( self, pattern=None, separator=None ):
        self.pattern = "(\w+: \W*\d+.\d+);" if not pattern else pattern
        self.separator = "\s*:\s*" if not separator else separator

    def parse( self, entry ):
        result = {}
        for i in findall( self.pattern, entry ):
            k,v = split( self.separator, i )
            result[k] = v
        return self.Entry( result )


    class Entry( object ):
        def __init__( self, data ):
            self.data = data

        def is_valid( self, required_fields=FIELDS ):
            result = True
            for field in required_fields:
                result &= self.data.has_key(field)
            return result

        def to_database( self ):
            values = [time.time()]
            values += [ self.data[f] for f in FIELDS ]

            database.execute(
                """ INSERT INTO krydderino VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? ) """,
                ( values )
            )
            database.commit()


if __name__ == "__main__":

    receiver = Receiver()

    # database.execute( """ DROP TABLE IF EXISTS krydderino """ )

    database.execute(
        """ CREATE TABLE IF NOT EXISTS krydderino (
                timestamp TIME UNIQUE PRIMARY KEY,
                ph FLOAT,
                ec FLOAT,
                temp_dry FLOAT,
                humidity_dry FLOAT,
                temp_wet FLOAT,
                fan_dry FLOAT,
                fan_wet FLOAT,
                fogger FLOAT
        )
        """
    )

    # [+] search and handshake
    serial = Serial( SERIAL_PORT, SERIAL_BAUDRATE, timeout=3 )
    serial.close()
    serial.open()

    try:
        while True:
            data = serial.readline()
            entry = receiver.parse( data )
            if entry.is_valid():
                entry.to_database()
    except KeyboardInterrupt:
        print database.execute( """ SELECT * FROM krydderino """ ).fetchall()

        database.close()
        serial.close()

    """
    except SerialException:
        pass
        # reconnect
    """