import freegs4e


class Machine(freegs4e.machine.Machine):
    """Same as freegs4e.machine.Machine.
    It can have an additional freegs4e.machine.Wall object which specifies the limiter's properties.
    """

    def __init__(self, coils, wall=None, limiter=None):
        """Instantiates the Machine, same as freegs4e.machine.Machine.

        Parameters
        ----------
        coils : FreeGS4E coils[(label, Coil|Circuit|Solenoid]
            List of coils
        wall : FreeGS4E machine.Wall object
            It is only used to display the wall in plots.
        limiter : FreeGS4E machine.Wall object
            This is the limiter. Used to define limiter plasma configurations.
        """
        super().__init__(coils, wall)
        self.limiter = limiter
