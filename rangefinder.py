# HRLV MaxSonar EZ
# 2.5v to 5.5v
# Scaling factor = Vcc / 5120 per mm; 5V = ~0.977mV per mm
# Model MB1013

import wpilib

class Maxbotultrasonic(wpilib.SensorBase):
    def Maxbotultrasonic(self, _channel):
        self.kin_to_cm = 2.54
        self.kuse_units = True
        self.kmin_voltage = 0
        self.kvoltage_range = 5.0 - self.kmin_voltage
        self.kmin_distance = 3.0
        self.kdistance_range = 60.0 - self.kmin_distance
        self.kchannel = wpilib.AnalogInput(_channel)

    def GetVoltage(self):
        return self.kchannel.getVoltage()

    def GetRangeInInches(self):
        range = self.kchannel.getVoltage()
        if not self.kuse_units:
            return -1.0
        elif range < self.kmin_voltage:
            return -2.0

        range = (range - self.kmin_voltage) / self.kvoltage_range
        range = (range * self.kdistance_range) + self.kmin_distance
        range *= self.kin_to_cm
        range = str(round(range, 2))
        return range

    def GetRangeInCM(self):
        range = float(Maxbotultrasonic.GetRangeInInches(self))
        range *= self.kin_to_cm

        return str(round(range, 2))
