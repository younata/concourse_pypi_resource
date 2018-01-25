# Concourse PyPi Resource

Concourse resource for querying PyPi

## Resource Type Configuration

```
resource_types:
  - name: pypi
    type: docker-image
    source:
      repository: younata/concourse-pypi-resource
      tag: latest
```

## Source Configuration

- `package`: _Required_. The Python package to check for.

## Behavior

### `check`: Check for new version

The resource will fetch the package specified in `package` and will items by their version.
