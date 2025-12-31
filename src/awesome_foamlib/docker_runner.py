"""Docker-based OpenFOAM runner using Docker SDK."""

import logging
import os
from pathlib import Path
from typing import cast

import docker
from docker.errors import ContainerError, DockerException, ImageNotFound

logger = logging.getLogger(__name__)


class DockerFoamRunner:
    """Run OpenFOAM commands in Docker containers using Docker SDK.

    This class provides a robust way to execute OpenFOAM commands in Docker containers
    by using the Docker SDK (docker-py) instead of subprocess calls. This approach
    offers better error handling, container state management, and extensibility.

    Args:
        image: Docker image to use for OpenFOAM. Defaults to "opencfd/openfoam-default:2406".

    Examples:
        >>> runner = DockerFoamRunner()
        >>> runner.run(Path("./cavity"), "blockMesh")
        >>> runner.run(Path("./cavity"), "icoFoam")

    """

    def __init__(self, image: str = "opencfd/openfoam-default:2406") -> None:
        """Initialize the Docker runner.

        Args:
            image: Docker image to use for OpenFOAM.

        """
        self.client = docker.from_env()
        self.image = image

    def run(
        self,
        case_path: Path,
        command: str,
        *,
        user: str | None = None,
    ) -> None:
        """Run an OpenFOAM command in a Docker container.

        Args:
            case_path: Path to the OpenFOAM case directory.
            command: OpenFOAM command to execute (e.g., "blockMesh", "icoFoam").
            user: User to run the command as. If None, uses host UID:GID to avoid
                permission issues.

        Raises:
            ContainerError: If the command fails in the container.
            ImageNotFound: If the specified Docker image is not found.
            DockerException: For other Docker-related errors.

        """
        case_path = Path(case_path).resolve()
        container_workdir = "/home/openfoam/project"

        # Use host UID:GID if user is not specified to avoid permission issues
        if user is None:
            uid = os.getuid()
            gid = os.getgid()
            user = f"{uid}:{gid}"

        # Construct command with OpenFOAM environment sourcing
        full_command = f"/bin/bash -c 'source /usr/lib/openfoam/openfoam*/etc/bashrc && {command}'"

        logger.info("Starting command: %s", command)

        try:
            container = self.client.containers.run(
                image=self.image,
                command=full_command,
                volumes={str(case_path): {"bind": container_workdir, "mode": "rw"}},
                working_dir=container_workdir,
                detach=True,  # Detach to stream logs
                user=user,
                remove=False,  # Don't auto-remove to allow log inspection
            )

            # Stream logs in real-time
            for line in container.logs(stream=True):
                logger.debug(line.decode("utf-8").rstrip())

            # Wait for container to finish
            result = container.wait()

            # Clean up
            container.remove()

            # Check exit code
            if result["StatusCode"] != 0:
                self._handle_failure(result["StatusCode"])

        except ContainerError:
            logger.exception("Container error")
            raise
        except ImageNotFound:
            logger.exception("Docker image not found")
            raise
        except DockerException:
            logger.exception("Docker error")
            raise
        except Exception:
            logger.exception("An error occurred")
            raise

    def _handle_failure(self, status_code: int) -> None:
        """Handle command failure.

        Args:
            status_code: Exit status code from the container.

        Raises:
            RuntimeError: Always raises with the status code.

        """
        msg = f"Command failed with status code {status_code}"
        raise RuntimeError(msg)

    def get_container_stats(self, container_id: str) -> dict[str, object]:
        """Get resource usage statistics for a running container.

        This can be used to monitor CPU, memory usage during OpenFOAM simulations.

        Args:
            container_id: ID of the running container.

        Returns:
            Dictionary containing container statistics.

        """
        container = self.client.containers.get(container_id)
        stats = container.stats(stream=False)
        return cast("dict[str, object]", stats)

    def pull_image(self) -> None:
        """Pull the Docker image if not already available locally."""
        logger.info("Pulling image: %s", self.image)
        try:
            self.client.images.pull(self.image)
            logger.info("Successfully pulled image: %s", self.image)
        except ImageNotFound:
            logger.exception("Image not found")
            raise
        except DockerException:
            logger.exception("Docker error while pulling image")
            raise
