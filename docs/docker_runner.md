# Docker SDK Runner

This document explains the implementation of `DockerFoamRunner`, a robust Docker SDK-based runner for OpenFOAM commands.

## Overview

`DockerFoamRunner` uses the Docker SDK for Python (`docker-py`) instead of subprocess calls to execute OpenFOAM commands in Docker containers. This approach provides:

- Better error handling through Python exceptions
- Direct Docker daemon communication
- Container state management as Python objects
- Extensibility for advanced features

## Advantages over Subprocess Approach

| Feature | Subprocess | Docker SDK |
|---------|------------|------------|
| **Readability** | Complex string manipulation | Clean Python API with object configuration |
| **Error Handling** | Manual exit code checking | Structured exceptions (`docker.errors`) |
| **Flexibility** | Requires local Docker CLI | Can connect to remote Docker hosts |
| **Overhead** | Minimal dependencies | Requires `docker` package |

## Basic Usage

```python
from pathlib import Path
from awesome_foamlib import DockerFoamRunner

# Initialize runner
runner = DockerFoamRunner()

# Run OpenFOAM commands
runner.run(Path("./cavity"), "blockMesh")
runner.run(Path("./cavity"), "icoFoam")
```

## Advanced Features

### Custom Docker Image

```python
runner = DockerFoamRunner(image="opencfd/openfoam-dev:latest")
```

### Pull Image Manually

```python
runner = DockerFoamRunner()
runner.pull_image()  # Ensure image is available before running
```

### Monitor Container Resources

```python
# Get CPU and memory usage during simulation
stats = runner.get_container_stats(container_id)
```

## Permission Handling

By default, `DockerFoamRunner` automatically uses the host user's UID and GID to prevent permission issues with generated files. This ensures files created in the container are owned by the host user, not root.

```python
# Automatic UID/GID handling (default)
runner.run(case_path, "blockMesh")

# Manual user specification
runner.run(case_path, "blockMesh", user="1000:1000")
```

## Implementation Details

### Environment Setup

OpenFOAM environment variables are sourced automatically:

```bash
/bin/bash -c 'source /usr/lib/openfoam/openfoam*/etc/bashrc && <command>'
```

### Volume Mounting

Case directories are mounted to `/home/openfoam/project` in the container with read-write permissions.

### Logging

The runner uses Python's logging module instead of print statements:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("awesome_foamlib")
```

## Future Enhancements

The Docker SDK approach enables advanced features:

1. **Resource Monitoring**: Track CPU, memory usage during simulations using `container.stats()`
2. **Parallel Execution**: Manage multiple containers with resource-aware scheduling
3. **Remote Execution**: Connect to remote Docker hosts for distributed computing
4. **Custom Networks**: Set up container networking for multi-process simulations

## Error Handling

All Docker operations raise specific exceptions:

- `ContainerError`: Command execution failed in container
- `ImageNotFound`: Specified Docker image not available
- `DockerException`: General Docker daemon errors

Example:

```python
from docker.errors import ImageNotFound

try:
    runner.run(case_path, "blockMesh")
except ImageNotFound:
    runner.pull_image()
    runner.run(case_path, "blockMesh")
```
