# smallstep-ca

## Initialization

The step-ca container will initialize itself on the first run.

1. start/initialize the CA
1. Download the root certificate and install to the system (stem ca bootstrap can do this, but trickier to run in a container)
1. create a certificate for step-ca host

## Generate a client certificate

```bash
sudo podman run --rm -it -p 80:8080 -v $(pwd):/home/step docker.io/smallstep/step-cli:0.30.2 step ca certificate navi.lan.internal navi.crt navi.key --http-listen :8080 --provisioner=acme
```
