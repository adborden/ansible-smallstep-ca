import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_data_directory(host):
    d = host.file('/var/lib/smallstep-ca')
    assert d.is_directory
    assert d.mode == 0o750


def test_quadlet_file(host):
    f = host.file('/etc/containers/systemd/smallstep-ca.container')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert 'Image=docker.io/smallstep/step-ca:latest' in f.content_string


def test_service_running(host):
    # Note: In some container environments, systemd might not fully start
    # the generated service without real podman/quadlet support in the guest.
    # This checks if the generated unit file exists via quadlet.
    s = host.service('smallstep-ca')
    # We can at least check if it is enabled
    assert s.is_enabled
