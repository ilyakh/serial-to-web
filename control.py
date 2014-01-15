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

        def __getitem__( self, key ):
            return self.data[key]

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
                values
            )
            database.commit()


class Strategy( object ):
    def __init__( self ):
        self.rules = []

    def add_rules( self, *rules ):
        for each_rule in rules:
            self.rules.append( each_rule )

    def __call__( self, entry ):
        for rule in self.rules:
            if not rule.evaluate( entry ):
                rule.react()


class Rule( object ):
    def __init__( self, state_index ):
        self.state_index = state_index


class DryAreaTemp( Rule ):
    def __call__( self, state ):
        if state[self.state_index] > 32:
            # start the fan
            pass
        elif state[self.state_index] < 20:
            # spray acid, release toxins
            pass
        else:
            # everything is ok, continue
            pass

class WetAreaTemp( Rule ):
    def __call__( self, state ):
        if state[self.state_index] < 20:
            pass

class DryAreaHumidity( Rule ):
    def __call__( self, state ):
        if state[self.state_index] > 60:
            # start the fan
            pass

class FogAcidity( Rule ):
    def __call__( self, state ):
        if state[self.state_index] > 6.2:
            pass
        elif state[self.state_index] < 5.5:
            pass

class WaterLevel( Rule ):
    def __call__( self, state ):
        if state[self.state_index] < 5.0:
            pass



# [+] faa farduino til aa lagre dato for siste gang vifta ble skrudd av





if __name__ == "__main__":

    receiver = Receiver()

    database.execute( """ DROP TABLE IF EXISTS krydderino """ )

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

    # [+] port search and handshake
    serial = Serial( SERIAL_PORT, SERIAL_BAUDRATE, timeout=3 )
    serial.close()
    serial.open()


    # initialization of strategy
    strategy = Strategy()
    #strategy.add_rules(
    #    WetAreaTemp(  ),
    #    DryAreaTemp(),
    #    DryAreaHumidity(),
    #    FogAcidity(),
    #)

    while True:
        try:
            data = serial.readline()
            entry = receiver.parse( data )
            if entry.is_valid():
                entry.to_database()
                # Controller( entry )

        except KeyboardInterrupt:
            database.close()
            serial.close()
        except SerialException:
            time.sleep( RECONNECT_DELAY )
            serial.open()