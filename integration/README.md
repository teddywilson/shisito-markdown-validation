# Shisito Integration Tests

This directory serves as a test Shisito project. Integration tests will be ran against this directory as if it's its own repository during presubmit.

To run locally:
```
Docker build -t shisito .
Docker run \
  -v /Path/to/shisito/integration:/github/workspace \
  shisito \
  RUN
```
