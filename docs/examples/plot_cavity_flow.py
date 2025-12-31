"""Lid-Driven Cavity Flow using foamlib.

=====================================

This example demonstrates how to set up and run the classic lid-driven cavity flow
simulation using foamlib with OpenFOAM and visualize results with PyVista.

The cavity flow is a standard benchmark problem in computational fluid dynamics where
the top wall of a square cavity moves with a constant velocity while all other walls
are stationary.

This example copies the OpenFOAM tutorial case and uses foamlib to manage and run
the simulation.

**Requirements:**

- OpenFOAM installed via APT: ``sudo apt install openfoam openfoam-examples``
- Or openfoam-app: https://github.com/gerlero/openfoam-app

**Reference:** OpenFOAM tutorial at ``tutorials/incompressible/icoFoam/cavity/cavity``
"""

# %%
# Setup and Imports
# -----------------
# Import necessary libraries for case setup, simulation, and visualization.

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)
# %%
# Download Tutorial Data
# ----------------------
# Download OpenFOAM cavity tutorial if not available locally.
