import os
import pytest
import freegs
import numpy as np

os.environ["ACTIVE_COILS_PATH"] = "./machine_configs/MAST-U/active_coils.pickle"
os.environ["PASSIVE_COILS_PATH"] = "./machine_configs/MAST-U/passive_coils.pickle"
os.environ["WALL_PATH"] = "./machine_configs/MAST-U/wall.pickle"
os.environ["LIMITER_PATH"] = "./machine_configs/MAST-U/limiter.pickle"

import freegsnke.jtor_update as jtor
from freegsnke import build_machine


@pytest.fixture()
def create_machine():
    tokamak = build_machine.tokamak()

    # Creates equilibrium object and initializes it with
    # a "good" solution
    # plasma_psi = np.loadtxt('plasma_psi_example.txt')
    eq = freegs.Equilibrium(
        tokamak=tokamak,
        # domains can be changed
        Rmin=0.1,
        Rmax=2.0,  # Radial domain
        Zmin=-2.2,
        Zmax=2.2,  # Height range
        # grid resolution can be changed
        nx=65,
        ny=129,  # Number of grid points
        # psi=plasma_psi[::2,:])
    )
    return eq, tokamak


def test_profiles_PaxisIp(create_machine):
    """Tests that the profiles have the xpt, opt and jtor attributes."""
    eq, tokamak = create_machine

    profiles = jtor.ConstrainPaxisIp(
        eq,
        tokamak.limiter,
        8.1e3,  # Plasma pressure on axis [Pascals]
        6.2e5,  # Plasma current [Amps]
        0.5,  # vacuum f = R*Bt
        alpha_m=1.8,
        alpha_n=1.2,
    )

    profiles.Jtor(eq.R, eq.Z, eq.psi())
    assert (
        hasattr(profiles, "xpt")
        and hasattr(profiles, "opt")
        and hasattr(profiles, "jtor")
    ), "The profiles object does not have the xpt, opt and jtor attributes"


def test_profiles_BetapIp(create_machine):
    """Tests that the profiles have the xpt, opt and jtor attributes."""
    eq, tokamak = create_machine

    profiles = jtor.ConstrainBetapIp(
        eq,
        tokamak.limiter,
        8.1e3,  # Plasma pressure on axis [Pascals]
        6.2e5,  # Plasma current [Amps]
        0.5,  # vacuum f = R*Bt
    )

    profiles.Jtor(eq.R, eq.Z, eq.psi())
    assert (
        hasattr(profiles, "xpt")
        and hasattr(profiles, "opt")
        and hasattr(profiles, "jtor")
    ), "The profiles object does not have the xpt, opt and jtor attributes"
