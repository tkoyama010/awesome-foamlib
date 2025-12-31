"""Download utilities for OpenFOAM tutorial data."""

import logging
import shutil
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)


def download_cavity_tutorial(target_dir: Path) -> Path:
    """Download or copy OpenFOAM cavity tutorial to a specific directory.

    Downloads the cavity tutorial case files to target_dir directly (not to a subdirectory).
    First checks system installation, then falls back to downloading from GitHub.

    Parameters
    ----------
    target_dir : Path
        Directory where tutorial files will be placed (must not exist or be empty)

    Returns
    -------
    Path
        Path to the tutorial directory (same as target_dir)

    """
    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # Check if already set up and valid
    if (target_dir / "system" / "controlDict").exists():
        logger.info("Using existing tutorial at: %s", target_dir)
        return target_dir

    # Check system installation first
    system_tutorial = Path(
        "/usr/share/doc/openfoam-examples/examples/incompressible/icoFoam/cavity/cavity",
    )

    if system_tutorial.exists() and (system_tutorial / "system" / "controlDict").exists():
        logger.info("Copying tutorial from system installation: %s", system_tutorial)
        try:
            # Copy contents into target_dir
            for item in system_tutorial.iterdir():
                if item.is_dir():
                    shutil.copytree(item, target_dir / item.name, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, target_dir / item.name)

            # Verify the copy was successful
            if (target_dir / "system" / "controlDict").exists():
                logger.info("Tutorial copied successfully to: %s", target_dir)
                return target_dir
            logger.warning("System copy incomplete, falling back to download")
        except (OSError, shutil.Error) as e:
            logger.warning("Failed to copy from system: %s", e)

    # Download from GitHub as fallback
    logger.info("Downloading tutorial from GitHub...")

    # Create directory structure
    (target_dir / "0").mkdir(exist_ok=True)
    (target_dir / "constant").mkdir(exist_ok=True)
    (target_dir / "system").mkdir(exist_ok=True)

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

    download_errors = []
    for remote_path, local_path in files_to_download.items():
        url = base_url + remote_path
        local_file = target_dir / local_path

        try:
            logger.info("Downloading %s...", remote_path)
            urllib.request.urlretrieve(url, local_file)  # noqa: S310
        except (urllib.error.URLError, OSError) as e:
            error_msg = f"Failed to download {remote_path}"
            logger.exception(error_msg)
            download_errors.append(f"{error_msg}: {e}")

    # Verify download was successful
    if not (target_dir / "system" / "controlDict").exists():
        # Clean up partial download
        shutil.rmtree(target_dir, ignore_errors=True)
        msg = (
            "Failed to download OpenFOAM tutorial. Errors: " + "; ".join(download_errors)
            if download_errors
            else "controlDict not found after download"
        )
        raise RuntimeError(msg)

    logger.info("Tutorial downloaded successfully to: %s", target_dir)
    return target_dir
