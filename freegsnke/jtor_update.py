import freegs
import numpy as np
from freegs import critical
from . import limiter_func
from . import plasma_grids


class ConstrainBetapIp(freegs.jtor.ConstrainBetapIp):
    """FreeGS profile class with a few modifications, to:
    - retain memory of critical point calculation;
    - deal with limiter plasma configurations

    """

    def __init__(self, eq, limiter, *args, **kwargs):
        """Instantiates the object.

        Parameters
        ----------
        mask_inside_limiter : np.array
            Boole mask, it is True inside the limiter. Same size as full domain grid: (eq.nx, eq.ny)
        """
        super().__init__(*args, **kwargs)

        self.limiter_handler = limiter_func.Limiter_handler(eq, limiter)
        self.limiter_mask_out = plasma_grids.make_layer_mask(self.limiter_handler.mask_inside_limiter, layer_size=1)
        self.mask_inside_limiter = self.limiter_handler.mask_inside_limiter

        
        if not hasattr(self, 'fast'):
            self.Jtor = self._Jtor
        else:
            self.Jtor = self.Jtor_fast

    def _Jtor(self, R, Z, psi, psi_bndry=None):
        """Replaces the original FreeGS Jtor method if FreeGSfast is not available."""
        self.jtor = super().Jtor(R, Z, psi, psi_bndry)
        self.opt, self.xpt = critical.find_critical(R, Z, psi)

        self.diverted_core_mask = self.jtor>0
        self.psi_bndry, mask, self.limiter_flag = self.limiter_handler.core_mask_limiter(psi,
                                                                                        self.xpt[0][2],
                                                                                        self.diverted_core_mask,
                                                                                        self.limiter_mask_out,
                                                                                        )
        self.jtor = super().Jtor(R, Z, psi, self.psi_bndry)
        return self.jtor

    def Jtor_fast(self, R, Z, psi, psi_bndry=None):
        """Used when FreeGSfast is available."""
        self.diverted_core_mask = super().Jtor_part1(R, Z, psi, psi_bndry)
        if self.diverted_core_mask is None:
            # print('no xpt')
            self.psi_bndry, self.limiter_core_mask, self.flag_limiter = psi_bndry, None, False
        else: 
            self.psi_bndry, self.limiter_core_mask, self.flag_limiter = self.limiter_handler.core_mask_limiter(psi,
                                                                                                                self.psi_bndry,
                                                                                                                self.diverted_core_mask,
                                                                                                                self.limiter_mask_out,
                                                                                                                )
        self.jtor = super().Jtor_part2(R, Z, psi, self.psi_bndry, self.limiter_core_mask)
        return self.jtor
    
    
    

class ConstrainPaxisIp(freegs.jtor.ConstrainPaxisIp):
    """FreeGS profile class with a few modifications, to:
    - retain memory of critical point calculation;
    - deal with limiter plasma configurations

    """

    def __init__(self, eq, limiter, *args, **kwargs):
        """Instantiates the object.

        Parameters
        ----------
        eq : freeGS Equilibrium object
            Specifies the domain properties
        limiter : freeGS.machine.Wall object
            Specifies the limiter contour points
        """
        super().__init__(*args, **kwargs) 
        
        self.limiter_handler = limiter_func.Limiter_handler(eq, limiter)
        self.limiter_mask_out = plasma_grids.make_layer_mask(self.limiter_handler.mask_inside_limiter, layer_size=1)
        self.mask_inside_limiter = self.limiter_handler.mask_inside_limiter
        
        if not hasattr(self, 'fast'):
            self.Jtor = self._Jtor
        else:
            self.Jtor = self.Jtor_fast

    def _Jtor(self, R, Z, psi, psi_bndry=None):
        """Replaces the original FreeGS Jtor method if FreeGSfast is not available."""
        self.jtor = super().Jtor(R, Z, psi, psi_bndry)
        self.opt, self.xpt = critical.find_critical(R, Z, psi)

        self.diverted_core_mask = self.jtor>0
        self.psi_bndry, mask, self.limiter_flag = self.limiter_handler.core_mask_limiter(psi,
                                                                                        self.xpt[0][2],
                                                                                        self.diverted_core_mask,
                                                                                        self.limiter_mask_out,
                                                                                        )
        self.jtor = super().Jtor(R, Z, psi, self.psi_bndry)
        return self.jtor

    def Jtor_fast(self, R, Z, psi, psi_bndry=None):
        """Used when FreeGSfast is available."""
        self.diverted_core_mask = super().Jtor_part1(R, Z, psi, psi_bndry)
        if self.diverted_core_mask is None:
            # print('no xpt')
            self.psi_bndry, self.limiter_core_mask, self.flag_limiter = psi_bndry, None, False
        else: 
            self.psi_bndry, self.limiter_core_mask, self.flag_limiter = self.limiter_handler.core_mask_limiter(psi,
                                                                                                                self.psi_bndry,
                                                                                                                self.diverted_core_mask,
                                                                                                                self.limiter_mask_out,
                                                                                                                )
        self.jtor = super().Jtor_part2(R, Z, psi, self.psi_bndry, self.limiter_core_mask)
        return self.jtor