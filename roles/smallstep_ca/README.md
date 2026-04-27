# Ansible Role: smallstep_ca

This role deploys a `smallstep-ca` container using Podman Quadlet (`.container` file).

## Requirements

- Podman installed on the target host.
- Systemd version that supports Quadlet (Podman 4.4+).

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `smallstep_ca_image` | `docker.io/smallstep/step-ca:latest` | The container image to use. |
| `smallstep_ca_container_name` | `smallstep-ca` | Name of the container. |
| `smallstep_ca_data_dir` | `/var/lib/smallstep-ca` | Host directory for CA data. |
| `smallstep_ca_name` | `Smallstep CA` | Name of the CA. |
| `smallstep_ca_password` | `password` | Password for CA initialization. |
| `smallstep_ca_dns_names` | `[localhost, {{ ansible_fqdn }}]` | DNS names for the CA. |
| `smallstep_ca_service_name` | `smallstep-ca` | Systemd service name. |
| `smallstep_ca_systemd_dir` | `/etc/containers/systemd` | Directory for Quadlet files. |

## Example Playbook

```yaml
- hosts: servers
  become: true
  roles:
    - role: smallstep_ca
      vars:
        smallstep_ca_password: "secure-password-here"
        smallstep_ca_dns_names:
          - ca.example.com
          - localhost
```

## License

MIT
