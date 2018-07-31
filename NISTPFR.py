#!/usr/bin/env python

from scipy.optimize import fsolve
import numpy as np
import pyiast

def solverloading(Ntot, RT, phi, rho, PureIsotherms, guess, tolerance):
    #For non-breathing: calculates equilbrium condition for the fluid and solid cell.
    x0 = guess
    #options=optimset('Display','off');   % notify= only when not converged
    
    # Calculate equilibrium using Nc component balances: 
    # Multicomponent equilibrium is provided by IAST
    # Solve for equilibrium partial pressures given single-component isotherms and total N
    def equations(p):
        x = np.array(p)
        
        ads = list(pyiast.iast(p,PureIsotherms,verboseflag=False,warningoff=True))

        return ( [ phi*x_i/RT + (1.-phi)*rho*ads_i - Ntot_i for (x_i,ads_i,Ntot_i) in zip(x,ads,Ntot) ] )

    x = fsolve(equations,x0,xtol=tolerance)
    y = np.array(x)
    return y
