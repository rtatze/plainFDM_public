import numpy as np


# siehe auch Drohne-Code Unity
class PidRegler(object):

    def __init__(self):
        self.kpaElevator = .1
        self.kdaElevator = 5
        self.kpaAileron = .1
        self.kdaAileron = 6

    # Headline: Aileron
    def getAileronCommand(self, heading_Reference, heading_Current, heading_rollAngleCurrent,
                          heading_rollAngleRateCurrent, AileronCurrent):
        heading_rollAngleReference = self._outerLoopAileron(heading_Reference, heading_Current)
        AileronCommand = self._innerLoopAileron(heading_rollAngleReference, heading_rollAngleCurrent,
                                                heading_rollAngleRateCurrent, AileronCurrent)
        return AileronCommand

    def _outerLoopAileron(self, heading_Reference, heading_Current):
        heading_rollAngleReference = (heading_Current - heading_Reference) * 1.0  # Vorsteuerung als P-Regler
        return heading_rollAngleReference

    # innerLoop: heading_roll->Aileron
    def _innerLoopAileron(self, rollAngle_Reference, rollAngle_Current, rollAngleRateCurrent, AileronCurrent):
        diff_rollAngle = np.rad2deg(rollAngle_Reference - rollAngle_Current)
        AileronCommand = np.clip(diff_rollAngle * self.kpaAileron - rollAngleRateCurrent * self.kdaAileron,
                                 -1, 1)
        AileronCommand = AileronCommand + AileronCurrent
        AileronCommand = np.clip(AileronCommand, -15, 20)
        return AileronCommand

    # Headline: Elevator
    def getElevatorCommand(self, TASReference, TASCurrent, pitchAngleCurrent, pitchAngleRateCurrent, elevatorCurrent):
        pitchAngleReference = self._outerLoopElevator(TASReference, TASCurrent)
        elevatorCommand = self._innerLoopElevator(pitchAngleReference, pitchAngleCurrent, pitchAngleRateCurrent,
                                                  elevatorCurrent)
        return elevatorCommand

    def _outerLoopElevator(self, TASReference, TASCurrent):
        pitchAngleReference = (TASCurrent - TASReference) * 1.0  # Vorsteuerung als P-Regler
        return pitchAngleReference

    # innerLoop: Pitch->Elevator
    def _innerLoopElevator(self, pitchAngleReference, pitchAngleCurrent, pitchAngleRateCurrent, elevatorCurrent):
        diffPitchAngle = np.rad2deg(pitchAngleReference - pitchAngleCurrent)
        elevatorCommand = np.clip(diffPitchAngle * self.kpaElevator - pitchAngleRateCurrent * self.kdaElevator,
                                  -1, 1)
        elevatorCommand = elevatorCommand + elevatorCurrent
        elevatorCommand = np.clip(elevatorCommand, -26, 28)
        return elevatorCommand


def main():
    pid = PidRegler()
    print(pid.getElevatorCommand(70, 60, 0, 0, 0))


if __name__ == '__main__':
    main()
