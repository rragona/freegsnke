import numpy as np
import freegs
from freegs.gradshafranov import Greens

class NewtonKrylov:

    """Implementation of Newton Krylow algorithm for solving
    non linear forward static Grad Shafranov (GS) problems.

    The solution domain is set at instantiation time, through the 
    input freeGS equilibrium object.

    The non-linear solver itself is called using the 'solve' method.
    """
     
    def __init__(self, eq):

        """Instantiates the NewtonKrylov class.
        Based on the domain grid of the input equilibrium object, it prepares
            - the linear solver 'self.solver'
            - the response matrix of boundary grid points 'self.greens_boundary'


        Parameters
        ----------
        eq : a freeGS equilibrium object.
             The domain grid defined by (eq.R, eq.Z) is the solution domain 
             adopted for the GS problems. Calls to the nonlinear solver will
             use the grid domain set at instantiation time. Re-instantiation 
             is necessary in order to change the propertes of either grid or
             domain.

        """
     
   
        #eq is an Equilibrium instance, it has to have the same domain and grid as 
        #the ones the solver will be called on
        
        R = eq.R
        Z = eq.Z
        self.R = R
        self.Z = Z
        R_1D = R[:,0]
        Z_1D = Z[0,:]
        
        #for reshaping
        nx,ny = np.shape(R)
        self.nx = nx
        self.ny = ny
        
        #for integration
        dR = R[1, 0] - R[0, 0]
        dZ = Z[0, 1] - Z[0, 0]
        self.dRdZ = dR*dZ


        #linear solver for del*Psi=RHS with fixed RHS
        self.solver = freegs.multigrid.createVcycle(
            nx, ny, 
            freegs.gradshafranov.GSsparse4thOrder(eq.R[0,0], 
                                                  eq.R[-1,0], 
                                                  eq.Z[0,0], 
                                                  eq.Z[0,-1]), 
            nlevels=1, ncycle=1, niter=2, direct=True)


        # List of indices on the boundary
        bndry_indices = np.concatenate(
            [
                [(x, 0) for x in range(nx)],
                [(x, ny - 1) for x in range(nx)],
                [(0, y) for y in range(ny)],
                [(nx - 1, y) for y in range(ny)],
            ]
        )
        self.bndry_indices = bndry_indices
        
        # matrices of responses of boundary locations to each grid positions
        greenfunc = Greens(R[np.newaxis,:,:], 
                           Z[np.newaxis,:,:], 
                           R_1D[bndry_indices[:,0]][:,np.newaxis,np.newaxis], 
                           Z_1D[bndry_indices[:,1]][:,np.newaxis,np.newaxis])
        # Prevent infinity/nan by removing Greens(x,y,x,y) 
        zeros = np.ones_like(greenfunc)
        zeros[np.arange(len(bndry_indices)), bndry_indices[:,0], bndry_indices[:,1]] = 0
        self.greenfunc = greenfunc*zeros*self.dRdZ

        
        #RHS/Jtor
        self.rhs_before_jtor = -freegs.gradshafranov.mu0*eq.R
                
        
            
    def freeboundary(self, plasma_psi, tokamak_psi, profiles):
        """Imposes boundary conditions on set of boundary points. 

        Parameters
        ----------
        plasma_psi : np.array of size (eq.nx, eq.ny)
            magnetic flux due to the plasma
        tokamak_psi : np.array of size (eq.nx, eq.ny)
            magnetic flux due to the tokamak alone, including all metal currents,
            in both active coils and passive structures
        profiles : freeGS profile object
            profile object describing target plasma properties, 
            used to calculate jtor(plasma_psi)
        """

        #tokamak_psi is psi from the currents assigned to the tokamak coils in eq, ie.
        #tokamak_psi = eq.tokamak.calcPsiFromGreens(pgreen=eq._pgreen)
        
        #jtor and RHS given tokamak_psi above and the input plasma_psi
        self.jtor = profiles.Jtor(self.R, self.Z, tokamak_psi+plasma_psi)
        self.rhs = self.rhs_before_jtor*self.jtor
        
        #calculates and assignes boundary conditions, NOT von Haugenow but 
        #exactly as in freegs
        self.psi_boundary = np.zeros_like(self.R)
        psi_bnd = np.sum(self.greenfunc*self.jtor[np.newaxis,:,:], axis=(-1,-2))
       
        self.psi_boundary[:, 0] = psi_bnd[:self.nx]
        self.psi_boundary[:, -1] = psi_bnd[self.nx:2*self.nx]
        self.psi_boundary[0, :] = psi_bnd[2*self.nx:2*self.nx+self.ny]
        self.psi_boundary[-1, :] = psi_bnd[2*self.nx+self.ny:]

        self.rhs[0, :] = self.psi_boundary[0, :]
        self.rhs[:, 0] = self.psi_boundary[:, 0]
        self.rhs[-1, :] = self.psi_boundary[-1, :]
        self.rhs[:, -1] = self.psi_boundary[:, -1]
         
        
    # def F(self, plasma_psi, profiles, eq): #root problem on Psi
    #     self.freeboundary(plasma_psi, profiles, eq)
    #     return plasma_psi - self.solver(self.psi_boundary, self.rhs)
    
    def _F(self, plasma_psi): 
        """Nonlinear Grad Shafranov equation written as a root problem
        F(plasma_psi) \equiv [\delta* - J](plasma_psi)
        The plasma_psi that solves the Grad Shafranov problem satisfies
        F(plasma_psi) = [\delta* - J](plasma_psi) = 0

        
        Parameters
        ----------
        plasma_psi : np.array of size (eq.nx, eq.ny)
            magnetic flux due to the plasma

        Needs self.tokamak_psi and self.profiles.
        Both are set in the 'solve' call.
        
        Returns
        -------
        residual : np.array of size (eq.nx, eq.ny)
            residual of the GS equation
        """ 
        #same as above, but uses private profiles and tokamak_psi
        self.freeboundary(plasma_psi, self.tokamak_psi, self.profiles)
        return plasma_psi - self.solver(self.psi_boundary, self.rhs)
    

    def Arnoldi_iteration(self, plasma_psi, #trial plasma_psi
                                vec_direction, #first vector for psi basis, both are in 2Dformat
                                Fresidual=None, #residual of trial plasma_psi: F(plasma_psi)
                                n_k=10, #max number of basis vectors
                                conv_crit=.2, #add basis vector 
                                                #if orthogonal component is larger than
                                grad_eps=1 #infinitesimal step
                         ):
        
        nplasma_psi = np.linalg.norm(plasma_psi)

        #basis in Psi space
        Q = np.zeros((self.nx*self.ny, n_k+1))
        #orthonormal basis in Psi space
        Qn = np.zeros((self.nx*self.ny, n_k+1))
        #basis in grandient space
        G = np.zeros((self.nx*self.ny, n_k+1))
        
        
        
        if Fresidual is None:
            Fresidual = self._F(plasma_psi)
        nFresidual = np.linalg.norm(Fresidual)
        
        
        n_it = 0
        #control on whether to add a new basis vector
        arnoldi_control = 1
        #use at least 3 orthogonal terms, but not more than n_k
        while arnoldi_control*(n_it<n_k)>0:
            grad_coeff = grad_eps*nplasma_psi/np.linalg.norm(vec_direction)*nFresidual/(n_it+1)**1.2

            candidate_dpsi = vec_direction*grad_coeff
            ri = self._F(plasma_psi + candidate_dpsi)
            candidate_usable = ri - Fresidual
            lvec_direction = candidate_usable.reshape(-1)


            # if ((np.linalg.norm(candidate_usable)/nFresidual)<2)+((np.linalg.norm(candidate_usable)/nFresidual)>10):
            #     print('using di factor = ', 2*(nFresidual/np.linalg.norm(candidate_usable)))
            #     candidate_dpsi *= 2*(nFresidual/np.linalg.norm(candidate_usable))
            #     ri = self._F(plasma_psi + candidate_dpsi)
            #     candidate_usable = ri - Fresidual


            Q[:,n_it] = candidate_dpsi.reshape(-1)
            #print('dcurrent = ', Q[:,n_it])

            Qn[:,n_it] = Q[:,n_it]/np.linalg.norm(Q[:,n_it])
            
            
            # vec_direction = candidate_usable.copy()
            # lvec_direction = vec_direction.reshape(-1)
            #print('usable/residual = ', np.linalg.norm(vec_direction)/nFresidual)
            # if verbose_currents:
            #     print('trial dI = ',Q[:,n_it])
            #     print('associated residual to use = ', vec_direction)
            G[:,n_it] = lvec_direction
            n_it += 1

            #orthogonalize residual 
            lvec_direction -= np.sum(np.sum(Qn[:,:n_it]*lvec_direction[:,np.newaxis], axis=0, keepdims=True)*Qn[:,:n_it], axis=1)
            vec_direction = lvec_direction.reshape(self.nx, self.ny)

            #check if more terms are needed
            #arnoldi_control = (np.linalg.norm(vec_direction)/nFresidual > conv_crit)
            self.G = G[:,:n_it]
            self.Q = Q[:,:n_it]
            self.dpsi(Fresidual, G=self.G, Q=self.Q, clip=3)
            rel_unexpl_res = np.linalg.norm(self.eplained_res.reshape(self.nx,self.ny)+Fresidual)/nFresidual
            #print('relative_unexplained_residual = ', rel_unexpl_res)
            arnoldi_control = (rel_unexpl_res > conv_crit)

        # #make both basis available
        # self.Q = Q[:,:n_it]
        # self.G = G[:,:n_it]


    

    def dpsi(self, res0, G, Q, clip=10):
        #solve the least sq problem in coeffs: min||G.coeffs+res0||^2
        self.coeffs = np.matmul(np.matmul(np.linalg.inv(np.matmul(G.T, G)),
                                     G.T), -res0.reshape(-1))
        self.eplained_res = np.sum(G*self.coeffs[np.newaxis,:], axis=1)                             
        self.coeffs = np.clip(self.coeffs, -clip, clip)
        #get the associated step in psi space
        self.valdpsi = np.sum(Q*self.coeffs[np.newaxis,:], axis=1).reshape(self.nx,self.ny)
        #dpsi *= self.boundary_mask
        return self.valdpsi

    
    #this is the solver itself
    #solves the forward GS problem: given 
    # - the set of active coil currents as in eq.tokamak,
    # - the plasma properties assigned by the object "profiles"
    # finds the equilibrium plasma_psi and assigns it to eq
    # The starting trial_plasma_psi is eq.plasma_psi
    def solve(self, eq, 
                    profiles,
                    rel_convergence=1e-6, 
                    n_k=8, #this is a good compromise between convergence and speed
                    conv_crit=.15, 
                    grad_eps=.5,
                    clip=10, #maximum absolute value of coefficients in psi space
                    #verbose=True,
                    max_iter=30 #after these it just stops
                    #,conv_history=False #returns relative convergence
                    ):
        
        # rel_c_history = []
        
        # print('starting NK')
        trial_plasma_psi = eq.plasma_psi
        self.profiles = profiles
        self.tokamak_psi = eq.tokamak.calcPsiFromGreens(pgreen=eq._pgreen)
        
        res0 = self._F(trial_plasma_psi)
        rel_change = np.amax(np.abs(res0))
        rel_change /= (np.amax(trial_plasma_psi)-np.amin(trial_plasma_psi))
        # rel_c_history.append(rel_change)
        if rel_change>.1:
            print('Warning: initial relative change is too high at', rel_change)
            print('NK will likely fail')
        # if verbose:
        #     print('rel_change_0', rel_change)
            
        it=0
        while rel_change>rel_convergence and it<max_iter:
            # print(rel_change)
            self.Arnoldi_iteration(trial_plasma_psi, 
                                   res0, #starting vector in psi space is the residual itself
                                   res0, #F(trial_plasma_psi) already calculated
                                   n_k, conv_crit, grad_eps)
            dpsi = self.dpsi(res0, self.G, self.Q, clip)
            # print(self.coeffs)
            trial_plasma_psi += dpsi
            res0 = self._F(trial_plasma_psi)
            rel_change = np.amax(np.abs(res0))
            rel_change /= (np.amax(trial_plasma_psi)-np.amin(trial_plasma_psi))
            # rel_c_history.append(rel_change)
            # if verbose:
            #     print(rel_change, 'coeffs=', self.coeffs)
            
            it += 1
        
        # update eq with new solution
        eq.plasma_psi = trial_plasma_psi

        # update plasma current
        eq._current = np.sum(profiles.jtor)*self.dRdZ
        
        #if max_iter was hit, then message:
        if not it<max_iter:
            print('failed to converge with less than {} iterations'.format(max_iter))
            print(f'last relative change = {rel_change}')
            
        # if conv_history:
        #     return np.array(rel_c_history)