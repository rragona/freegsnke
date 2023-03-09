import numpy as np

class implicit_euler_solver:
    # implicit Euler time stepper for the linearized circuit equation
    # solves an equation of the type
    # MIdot + RI = F
    # with generic M, R and F
    # in practice, uses
    # I(t+dt) = (M-1Rdt + 1)^-1 . (M-1F + I(t))
    
    
    def __init__(self, Mmatrix, Rmatrix, full_timestep, max_internal_timestep):

        self.Mmatrix = Mmatrix
        self.Mmatrixm1 = np.linalg.inv(Mmatrix)

        self.Rmatrix = Rmatrix

        self.set_timesteps(full_timestep, max_internal_timestep)
        
        self.dims = np.shape(Mmatrix)[0]
            

        #dummy voltage vector
        self.empty_U = np.zeros(self.dims)


    def set_Mmatrix(self, Mmatrix):
        self.Mmatrix = Mmatrix
        self.Mmatrixm1 = np.linalg.inv(Mmatrix)
        self.calc_inverse_operator()

    def set_Rmatrix(self, Rmatrix):
        self.Rmatrix = Rmatrix
        self.calc_inverse_operator()
    
    def calc_inverse_operator(self, ):
        self.inverse_operator = np.linalg.inv(np.eye(np.shape(self.Mmatrix)[0]) + self.internal_timestep*self.Mmatrixm1@self.Rmatrix)

    def set_timesteps(self, full_timestep, max_internal_timestep):
        self.full_timestep = full_timestep
        self.max_internal_timestep = max_internal_timestep
        self.n_steps = int(full_timestep/max_internal_timestep + .999)
        self.internal_timestep = self.full_timestep/self.n_steps 
        self.calc_inverse_operator()



    def internal_stepper(self, It, Mm1forcing):
        # executes on self.internal_timestep
        # I(t+dt) = (M-1Rdt + 1)^-1 . (Mm1forcing + I(t))
        # note the different definition of the forcing term with respect to full_stepper
        Itpdt = self.inverse_operator@(Mm1forcing*self.internal_timestep + It)
        return Itpdt

    def full_stepper(self, It, forcing):
        # executes on self.full_timestep
        # by repeating over self.n_steps
        # I(t+dt) = (M-1Rdt + 1)^-1 . (M-1.forcing + I(t))
        # note the different definition of the forcing term with respect to internal_stepper

        Mm1forcing = np.dot(self.Mmatrixm1, forcing)
        for _ in range(self.n_steps):
            It = self.internal_stepper(It, Mm1forcing)
        
        return It
