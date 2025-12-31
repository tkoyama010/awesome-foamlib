"""Download utilities for OpenFOAM tutorial data."""

import logging
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)


def download_cavity_tutorial(target_dir: Path) -> Path:
    """Download OpenFOAM cavity tutorial from GitHub.

    Parameters
    ----------
    target_dir : Path
        Directory to extract tutorial files

    Returns
    -------
    Path
        Path to the extracted cavity tutorial directory

    """
    # Base URL for downloading tutorial files
    cavity_dir = target_dir / "cavity"

    # If already exists, return it
    if cavity_dir.exists() and (cavity_dir / "system" / "controlDict").exists():
        logger.info("Using existing tutorial at: %s", cavity_dir)
        return cavity_dir

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

    base_url = (
        "https://raw.githubusercontent.com/OpenFOAM/OpenFOAM-dev/master/"
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
            raise

    logger.info("Tutorial downloaded to: %s", cavity_dir)
    return cavity_dir
