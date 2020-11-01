# Shisito test project

This is a (local) test Shisito project used for running integration tests against the framework itself.

To run these tests, build the Docker image in the root directory of the project, and mount the test directory as a volume.

For example:
```
Docker build -t shisito .
Docker run \
  -v /Users/theodorewilson/dev/shisito/test:/github/workspace \ 
  shisito
```

There is probably a better way to do all of this, but this will work for now.