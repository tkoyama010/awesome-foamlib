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
import os
import shutil
import tempfile
from pathlib import Path

import foamlib
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
from scipy.interpolate import griddata

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# %%
# Copy OpenFOAM Tutorial Case
# ----------------------------
# Copy the cavity tutorial from the installed OpenFOAM examples.

# Path to the installed cavity tutorial
tutorial_path = Path(
    "/usr/share/doc/openfoam-examples/examples/incompressible/icoFoam/cavity/cavity",
)

# Create a temporary working directory
work_dir = Path(tempfile.mkdtemp(prefix="cavity_"))
case_dir = work_dir / "cavity"

# Copy the entire tutorial case
shutil.copytree(tutorial_path, case_dir)
logger.info("Copied tutorial case to: %s", case_dir)

# Reduce simulation time if running on ReadTheDocs (to avoid timeout)
if os.environ.get("READTHEDOCS") == "True":
    controldict_path = case_dir / "system" / "controlDict"
    controldict_text = controldict_path.read_text()
    # Reduce endTime from 0.5 to 0.1 and writeInterval from 20 to 10
    controldict_text = controldict_text.replace("endTime         0.5;", "endTime         0.1;")
    controldict_text = controldict_text.replace("writeInterval   20;", "writeInterval   10;")
    controldict_path.write_text(controldict_text)
    logger.info("Reduced simulation time for ReadTheDocs build")

# List case structure
logger.info("\nCase directory structure:")
for item in case_dir.rglob("*"):
    if item.is_file():
        logger.info("  %s", item.relative_to(case_dir))

# %%
# Initialize foamlib Case
# -----------------------
# Create a FoamCase object for case management.

case = foamlib.FoamCase(case_dir)
logger.info("\nfoamlib case initialized: {case.path}")

# Display case information
logger.info("Application: icoFoam")
logger.info("Case contains: {len(list(case_dir.rglob('*')))} files/directories")

# %%
# Generate Mesh with foamlib
# ---------------------------
# Run blockMesh to generate the computational mesh.

logger.info("\nGenerating mesh with blockMesh...")
case.block_mesh()
logger.info("Mesh generation complete!")

# Check mesh files
mesh_dir = case_dir / "constant" / "polyMesh"
if mesh_dir.exists():
    mesh_files = [f.name for f in mesh_dir.iterdir() if f.is_file()]
    logger.info("Mesh files created: {mesh_files}")

# %%
# Run icoFoam Solver with foamlib
# --------------------------------
# Execute the incompressible laminar flow solver.

logger.info("\nRunning icoFoam solver...")
logger.info("This may take a few moments...")
case.run()
logger.info("Simulation completed successfully!")

# Display available time steps
time_steps = [str(t) for t in case.times]
logger.info("\nSimulation wrote {len(time_steps)} time steps:")
logger.info("  Times: {time_steps}")

# %%
# Read Results with foamlib
# --------------------------
# Extract velocity and pressure fields at the final time step.

final_time = case.times[-1]
logger.info("\nReading results at t = {final_time}s")

# Access field data using foamlib
U_field = case[final_time]["U"]
p_field = case[final_time]["p"]
cell_centers = case[final_time].cell_centres

logger.info("Velocity field shape: {U_field.shape}")
logger.info("Pressure field shape: {p_field.shape}")
logger.info("Number of cells: {len(cell_centers)}")

# Calculate velocity magnitude
U_mag = np.sqrt(U_field[:, 0] ** 2 + U_field[:, 1] ** 2 + U_field[:, 2] ** 2)
logger.info("Max velocity magnitude: {U_mag.max():.4f} m/s")

# %%
# Create PyVista Mesh for Visualization
# --------------------------------------
# Convert OpenFOAM data to PyVista format.

# Create PyVista point cloud from cell centers
cloud = pv.PolyData(cell_centers)

# Add scalar fields
cloud["U_magnitude"] = U_mag
cloud["pressure"] = p_field
cloud["U_x"] = U_field[:, 0]
cloud["U_y"] = U_field[:, 1]
cloud["U_z"] = U_field[:, 2]

logger.info("\nPyVista mesh created:")
logger.info("  Points: {cloud.n_points}")
logger.info("  Arrays: {cloud.array_names}")

# %%
# 3D Visualization with PyVista
# ------------------------------
# Create interactive 3D visualization of velocity and pressure fields.

plotter = pv.Plotter(shape=(1, 2), window_size=[1400, 600])

# Subplot 1: Velocity magnitude
plotter.subplot(0, 0)
plotter.add_mesh(
    cloud,
    scalars="U_magnitude",
    cmap="viridis",
    point_size=15,
    render_points_as_spheres=True,
    scalar_bar_args={"title": "Velocity Magnitude [m/s]", "vertical": True},
)
plotter.add_text("Velocity Magnitude", font_size=14, color="black")
plotter.view_xy()
plotter.camera.zoom(1.2)

# Subplot 2: Pressure field
plotter.subplot(0, 1)
plotter.add_mesh(
    cloud,
    scalars="pressure",
    cmap="RdBu_r",
    point_size=15,
    render_points_as_spheres=True,
    scalar_bar_args={"title": "Pressure [m²/s²]", "vertical": True},
)
plotter.add_text("Pressure Field", font_size=14, color="black")
plotter.view_xy()
plotter.camera.zoom(1.2)

plotter.show()

# %%
# Velocity Profile Analysis
# --------------------------
# Extract velocity profiles along the cavity centerlines for validation.

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Vertical centerline (x ≈ 0.05m)
tolerance = 0.01
vertical_mask = np.abs(cell_centers[:, 0] - 0.05) < tolerance
y_vert = cell_centers[vertical_mask, 1]
u_vert = U_field[vertical_mask, 0]

# Sort by y coordinate
idx = np.argsort(y_vert)
y_vert_sorted = y_vert[idx]
u_vert_sorted = u_vert[idx]

ax1.plot(u_vert_sorted, y_vert_sorted, "b-o", markersize=6, linewidth=2, label="CFD")
ax1.set_xlabel("U velocity [m/s]", fontsize=12)
ax1.set_ylabel("y [m]", fontsize=12)
ax1.set_title("U-velocity along vertical centerline", fontsize=13, fontweight="bold")
ax1.grid(visible=True, alpha=0.3, linestyle="--")
ax1.legend()
ax1.set_xlim([-0.3, 1.1])

# Horizontal centerline (y ≈ 0.05m)
horizontal_mask = np.abs(cell_centers[:, 1] - 0.05) < tolerance
x_horiz = cell_centers[horizontal_mask, 0]
v_horiz = U_field[horizontal_mask, 1]

# Sort by x coordinate
idx = np.argsort(x_horiz)
x_horiz_sorted = x_horiz[idx]
v_horiz_sorted = v_horiz[idx]

ax2.plot(x_horiz_sorted, v_horiz_sorted, "r-o", markersize=6, linewidth=2, label="CFD")
ax2.set_xlabel("x [m]", fontsize=12)
ax2.set_ylabel("V velocity [m/s]", fontsize=12)
ax2.set_title("V-velocity along horizontal centerline", fontsize=13, fontweight="bold")
ax2.grid(visible=True, alpha=0.3, linestyle="--")
ax2.legend()

plt.tight_layout()
plt.show()

# %%
# 2D Contour Plots with Matplotlib
# ---------------------------------
# Create publication-quality 2D contour plots.

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Create regular grid for interpolation
xi = np.linspace(0, 0.1, 100)
yi = np.linspace(0, 0.1, 100)
Xi, Yi = np.meshgrid(xi, yi)

# Interpolate data onto regular grid
U_mag_grid = griddata(cell_centers[:, :2], U_mag, (Xi, Yi), method="cubic")
p_grid = griddata(cell_centers[:, :2], p_field, (Xi, Yi), method="cubic")
Ux_grid = griddata(cell_centers[:, :2], U_field[:, 0], (Xi, Yi), method="cubic")
Uy_grid = griddata(cell_centers[:, :2], U_field[:, 1], (Xi, Yi), method="cubic")

# Plot 1: Velocity magnitude contours
im1 = axes[0, 0].contourf(Xi, Yi, U_mag_grid, levels=20, cmap="viridis")
axes[0, 0].contour(Xi, Yi, U_mag_grid, levels=10, colors="black", linewidths=0.5, alpha=0.3)
axes[0, 0].set_xlabel("x [m]", fontsize=11)
axes[0, 0].set_ylabel("y [m]", fontsize=11)
axes[0, 0].set_title("Velocity Magnitude", fontsize=12, fontweight="bold")
axes[0, 0].set_aspect("equal")
cbar1 = plt.colorbar(im1, ax=axes[0, 0])
cbar1.set_label("|U| [m/s]", fontsize=10)

# Plot 2: Pressure contours
im2 = axes[0, 1].contourf(Xi, Yi, p_grid, levels=20, cmap="RdBu_r")
axes[0, 1].contour(Xi, Yi, p_grid, levels=10, colors="black", linewidths=0.5, alpha=0.3)
axes[0, 1].set_xlabel("x [m]", fontsize=11)
axes[0, 1].set_ylabel("y [m]", fontsize=11)
axes[0, 1].set_title("Pressure Field", fontsize=12, fontweight="bold")
axes[0, 1].set_aspect("equal")
cbar2 = plt.colorbar(im2, ax=axes[0, 1])
cbar2.set_label("p [m²/s²]", fontsize=10)

# Plot 3: Streamlines
strm = axes[1, 0].streamplot(
    Xi,
    Yi,
    Ux_grid,
    Uy_grid,
    density=2.0,
    color=U_mag_grid,
    cmap="viridis",
    linewidth=1.5,
)
axes[1, 0].set_xlabel("x [m]", fontsize=11)
axes[1, 0].set_ylabel("y [m]", fontsize=11)
axes[1, 0].set_title("Streamlines", fontsize=12, fontweight="bold")
axes[1, 0].set_aspect("equal")
cbar3 = plt.colorbar(strm.lines, ax=axes[1, 0])
cbar3.set_label("|U| [m/s]", fontsize=10)

# Plot 4: Velocity vectors
skip = 3  # Show every 3rd vector for clarity
Q = axes[1, 1].quiver(
    cell_centers[::skip, 0],
    cell_centers[::skip, 1],
    U_field[::skip, 0],
    U_field[::skip, 1],
    U_mag[::skip],
    cmap="viridis",
    scale=5,
)
axes[1, 1].set_xlabel("x [m]", fontsize=11)
axes[1, 1].set_ylabel("y [m]", fontsize=11)
axes[1, 1].set_title("Velocity Vectors", fontsize=12, fontweight="bold")
axes[1, 1].set_aspect("equal")
cbar4 = plt.colorbar(Q, ax=axes[1, 1])
cbar4.set_label("|U| [m/s]", fontsize=10)

plt.tight_layout()
plt.show()

# %%
# Flow Statistics
# ---------------
# Calculate and display key flow statistics.

logger.info("\n%s", "=" * 50)
logger.info("FLOW STATISTICS")
logger.info("=" * 50)
logger.info("Maximum velocity magnitude: {U_mag.max():.4f} m/s")
logger.info("Minimum velocity magnitude: {U_mag.min():.4f} m/s")
logger.info("Average velocity magnitude: {U_mag.mean():.4f} m/s")
logger.info("Maximum pressure: {p_field.max():.6f} m²/s²")
logger.info("Minimum pressure: {p_field.min():.6f} m²/s²")
logger.info("Pressure range: {p_field.max() - p_field.min():.6f} m²/s²")
logger.info("=" * 50)

logger.info("\nCase directory preserved at: {case_dir}")
logger.info("You can inspect the results with ParaView or other post-processing tools.")

# %%
# Summary
# -------
# This example demonstrated a complete CFD workflow using foamlib:
#
# **Workflow Steps:**
#
# 1. **Case Setup**: Copied OpenFOAM tutorial case from system installation
# 2. **Mesh Generation**: Used ``case.block_mesh()`` to generate mesh
# 3. **Solver Execution**: Ran icoFoam with ``case.run()``
# 4. **Data Access**: Read fields using foamlib's ``case[time]["field"]`` interface
# 5. **Visualization**:
#    - PyVista for interactive 3D visualization
#    - Matplotlib for publication-quality 2D plots
#
# **Physical Insights:**
#
# The lid-driven cavity flow exhibits:
#
# - Primary vortex in the center of the cavity
# - Secondary vortices in the bottom corners (especially bottom-left)
# - Velocity maximum near the moving lid
# - Characteristic pressure distribution driven by centrifugal effects
#
# **Key Features of foamlib:**
#
# - **Pythonic Interface**: Natural Python API for OpenFOAM
# - **Easy Case Management**: Simple methods like ``block_mesh()`` and ``run()``
# - **Direct Data Access**: Access fields as NumPy arrays
# - **No Manual Parsing**: foamlib handles OpenFOAM file formats
#
# **References:**
#
# - foamlib documentation: https://github.com/gerlero/foamlib
# - PyVista documentation: https://docs.pyvista.org/
# - OpenFOAM User Guide: https://www.openfoam.com/documentation/user-guide
# - Cavity tutorial: https://www.openfoam.com/documentation/tutorial-guide/2-incompressible-flow/2.1-lid-driven-cavity-flow
