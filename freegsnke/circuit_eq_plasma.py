import numpy as np


class plasma_current:
    # implements the plasma circuit equation
    # in projection on Iy.T:
    # Iy.T/Ip (Myy Iydot + Mye Iedot + Rp Iy) = 0

    def __init__(self, plasma_grids, Rm12V, plasma_resistance_1d, Mye=None):

        self.Myy = plasma_grids.Myy()
        if Mye is None:
            self.Mye = (plasma_grids.Mey()).T
        else:
            self.Mye = Mye
        self.MyeRm12V = np.matmul(self.Mye, Rm12V)
        self.Ryy = plasma_resistance_1d
    
    # def reduced_Iy(self, full_Iy):
    #     Iy = full_Iy[self.mask_inside_limiter]
    #     return Iy


    # def Iydot(self, Iy1, Iy0, dt):
    #     full_Iydot = (Iy1-Iy0)/dt
    #     Iydot = self.reduced_Iy(full_Iydot)
    #     return Iydot


    def current_residual(self,  red_Iy0, 
                                red_Iy1,
                                red_Iydot,
                                Iddot):

        # residual = Iy0.T/Ip0 (Myy Iydot + Mey Iedot + Ryy Iy)
        # residual here = Iy0.T/Ip0 (Myy Iydot + Mey Rm12 V Iddot + Ryy Iy)/Rp0
        # where Rp0 =  Iy0.T/Ip0 Ryy Iy0/Ip0

        Ip0 = np.sum(red_Iy0)
        norm_red_Iy0 = red_Iy0/Ip0
        
        Fy = np.dot(self.Myy, red_Iydot)
        Fe = np.dot(self.MyeRm12V, Iddot)
        Fr = self.Ryy*red_Iy1
        Ftot = Fy+Fe+Fr

        residual = np.dot(norm_red_Iy0, Ftot)
        residual *= 1/np.sum(norm_red_Iy0*Fr)

        return residual

