from random import random

class TestSerial(object):
    def __init__( self, device, port, timeout ):
        self.device = device
        self.port = port

        # sensors
        self.TEMP_DRY = 25.0
        self.TEMP_WET = 20.0
        self.EC = 100.0
        self.PH = 5.2
        self.HUMIDITY_DRY = 50.0
        # actuators
        self.SOLENOID_PH_UP = 0.0
        self.SOLENOID_PH_DOWN = 0.0
        self.SOLENOID_NUTRIENT = 0.0
        self.FAN_DRY = 0.0
        self.FAN_WET = 0.0
        self.FOGGER = 0.0

    def open( self ):
        pass

    def close( self ):
        pass

    def write( self, query ):
        command, a, b = query.split( " " )

        if command == "SET":

            if a == "FAN_DRY":
                if int( b ) == 1:
                    self.FAN_DRY = 1.0
                elif int( b ) == 0:
                    self.FAN_DRY = 0.0
            elif a == "FAN_WET":
                if int( b ) == 1:
                    self.FAN_WET = 1.0
                elif int( b ) == 0:
                    self.FAN_WET = 0.0
            elif a == "SOLENOID_PH_DOWN":
                if int( b ) == 1:
                    self.SOLENOID_PH_DOWN = 1.0
                elif int( b ) == 0:
                    self.SOLENOID_PH_DOWN = 0.0
            elif a == "SOLENOID_PH_UP":
                if int( b ) == 1:
                    self.SOLENOID_PH_UP = 1.0
                elif int( b ) == 0:
                    self.SOLENOID_PH_UP = 0.0
            elif a == "SOLENOID_NUTRIENT":
                if int( b ) == 1:
                    self.SOLENOID_NUTRIENT = 1.0
                elif int( b ) == 0:
                    self.SOLENOID_NUTRIENT = 0.0

        elif command == "FETCH":
            print "(test_serial) 'fetch'-type commands are not supported"
        else:
            print "(test_serial) command was not recognized"

    def randomize_sensor_values( self ):
        self.TEMP_DRY += -random() if random() > 0.5 else random()
        self.TEMP_WET += -random() if random() > 0.5 else random()
        self.EC += -random() if random() > 0.5 else random()
        self.PH += -random() if random() > 0.5 else random()
        self.HUMIDITY_DRY += -random() if random() > 0.5 else random()


    def readline( self ):

        self.randomize_sensor_values()

        result = (
            "TEMP_DRY: {s.TEMP_DRY}; TEMP_WET: {s.TEMP_WET}; EC: {s.EC}; PH: {s.PH}; "
            "SOLENOID_PH_UP: {s.SOLENOID_PH_UP}; SOLENOID_PH_DOWN: {s.SOLENOID_PH_DOWN}; SOLENOID_NUTRIENT: {s.SOLENOID_NUTRIENT}; "
            "FAN_DRY: {s.FAN_DRY}; FAN_WET: {s.FAN_WET}; FOGGER: {s.FOGGER}; HUMIDITY_DRY: {s.HUMIDITY_DRY};"
        )

        return result.format(
            s=self
        )