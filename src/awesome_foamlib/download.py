"""Download utilities for OpenFOAM tutorial data."""

import logging
import shutil
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)


def download_cavity_tutorial(target_dir: Path) -> Path:
    """Download or copy OpenFOAM cavity tutorial.

    First checks system installation, then falls back to downloading from GitHub.

    Parameters
    ----------
    target_dir : Path
        Directory to extract tutorial files

    Returns
    -------
    Path
        Path to the cavity tutorial directory

    """
    cavity_dir = target_dir / "cavity"

    # If already exists in target, return it
    if cavity_dir.exists() and (cavity_dir / "system" / "controlDict").exists():
        logger.info("Using existing tutorial at: %s", cavity_dir)
        return cavity_dir

    # Check system installation first
    system_tutorial = Path(
        "/usr/share/doc/openfoam-examples/examples/incompressible/icoFoam/cavity/cavity",
    )

    if system_tutorial.exists():
        logger.info("Copying tutorial from system installation...")
        shutil.copytree(system_tutorial, cavity_dir)
        logger.info("Tutorial copied to: %s", cavity_dir)
        return cavity_dir

    # Download from GitHub as fallback
    logger.info("System tutorial not found, downloading from GitHub...")

    # Create tutorial directory structure
    cavity_dir.mkdir(parents=True, exist_ok=True)
    (cavity_dir / "0").mkdir(exist_ok=True)
    (cavity_dir / "constant").mkdir(exist_ok=True)
    (cavity_dir / "system").mkdir(exist_ok=True)

    # Download essential files
    files_to_download = {
        "system/controlDict": "system/controlDict",
        "system/fvSchemes": "system/fvSchemes",
        "system/fvSolution": "system/fvSolution",
        "system/blockMeshDict": "system/blockMeshDict",
        "0/U": "0/U",
        "0/p": "0/p",
        "constant/transportProperties": "constant/transportProperties",
    }

    # Try ESI OpenFOAM repository
    base_url = (
        "https://develop.openfoam.com/Development/openfoam/-/raw/master/"
        "tutorials/incompressible/icoFoam/cavity/cavity/"
    )

    for remote_path, local_path in files_to_download.items():
        url = base_url + remote_path
        local_file = cavity_dir / local_path

        try:
            logger.info("Downloading %s...", remote_path)
            urllib.request.urlretrieve(url, local_file)  # noqa: S310
        except Exception as e:
            logger.warning("Failed to download %s: %s", remote_path, e)
            # Clean up partial download
            if cavity_dir.exists():
                shutil.rmtree(cavity_dir)
            msg = (
                "Failed to download OpenFOAM tutorial. "
                "Please install openfoam-examples: "
                "sudo apt install openfoam-examples"
            )
            raise RuntimeError(msg) from e

    logger.info("Tutorial downloaded to: %s", cavity_dir)
    return cavity_dir
