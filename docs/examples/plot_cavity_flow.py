"""Lid-Driven Cavity Flow using foamlib.

=====================================

This example demonstrates how to set up and run the classic lid-driven cavity flow
simulation using foamlib with OpenFOAM and visualize results with PyVista.

The cavity flow is a standard benchmark problem in computational fluid dynamics where
the top wall of a square cavity moves with a constant velocity while all other walls
are stationary.

This example uses foamlib to download tutorial data, generate mesh, and visualize it.

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
import tempfile
from pathlib import Path

import foamlib
import pyvista as pv

from awesome_foamlib import download_cavity_tutorial

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# %%
# Download OpenFOAM Tutorial
# --------------------------
# Download the cavity tutorial from GitHub.

work_dir = Path(tempfile.mkdtemp(prefix="cavity_"))
case_dir = download_cavity_tutorial(work_dir)
logger.info("Tutorial downloaded to: %s", case_dir)

# %%
# Initialize foamlib Case and Generate Mesh
# ------------------------------------------
# Create a FoamCase object and run blockMesh to generate the computational mesh.

case = foamlib.FoamCase(case_dir)
logger.info("foamlib case initialized: %s", case.path)

# Generate mesh with blockMesh
logger.info("Generating mesh with blockMesh...")
case.block_mesh()
logger.info("Mesh generation complete!")

# %%
# Visualize Mesh with PyVista
# ----------------------------
# Read the OpenFOAM mesh and visualize it using PyVista.

# Read the mesh using foamlib
logger.info("Reading mesh with foamlib...")
mesh = case[0].mesh

# Get mesh points and cell connectivity
points = mesh.points
logger.info("Mesh contains %d points", len(points))

# Create PyVista mesh from OpenFOAM mesh
# Extract cell centers for visualization
cell_centers = mesh.cell_centres

# Create a PyVista point cloud from mesh points
point_cloud = pv.PolyData(points)

# Create a point cloud from cell centers
cell_cloud = pv.PolyData(cell_centers)

# %%
# Plot Mesh Points
# ----------------
# Visualize the mesh points in 3D.

plotter = pv.Plotter(window_size=(800, 600))
plotter.add_mesh(
    point_cloud,
    color="blue",
    point_size=5,
    render_points_as_spheres=True,
    label="Mesh Points",
)
plotter.add_mesh(
    cell_cloud,
    color="red",
    point_size=3,
    render_points_as_spheres=True,
    label="Cell Centers",
)
plotter.add_title("Cavity Mesh Visualization", font_size=14)
plotter.add_axes()
plotter.show_bounds(
    grid="front",
    location="outer",
    all_edges=True,
    xlabel="x [m]",
    ylabel="y [m]",
    zlabel="z [m]",
)
plotter.view_isometric()
plotter.show()

# %%
# Mesh Statistics
# ---------------
# Display mesh information.

logger.info("\nMesh statistics:")
logger.info("  Total points: %d", len(points))
logger.info("  Total cells: %d", len(cell_centers))
logger.info("  Domain bounds:")
logger.info("    x: [%.6f, %.6f] m", points[:, 0].min(), points[:, 0].max())
logger.info("    y: [%.6f, %.6f] m", points[:, 1].min(), points[:, 1].max())
logger.info("    z: [%.6f, %.6f] m", points[:, 2].min(), points[:, 2].max())

logger.info("\nMesh generation and visualization complete!")
logger.info("Case directory: %s", case_dir)
logger.info("Next step: Run simulation with case.run()")
