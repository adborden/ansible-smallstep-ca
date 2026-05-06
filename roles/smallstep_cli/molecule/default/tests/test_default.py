import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_smallstep_directory(host):
    d = host.file("/etc/smallstep")
    assert d.is_directory
    assert d.mode == 0o2750
    assert d.group == "cert-access"


def test_root_ca_exists(host):
    root = host.file("/etc/smallstep/root.crt")
    assert root.exists
    assert root.is_file
    assert root.mode == 0o644


def test_systemd_container_units(host):
    units = [
        "smallstep-cli-renew.container",
        "smallstep-cli-cleanup.container",
    ]
    for unit in units:
        f = host.file(f"/etc/containers/systemd/{unit}")
        assert f.exists
        assert f.is_file
        assert f.user == "root"
        assert f.group == "root"
        assert f.mode == 0o644

    # Specific check for daemon mode in renew
    renew = host.file("/etc/containers/systemd/smallstep-cli-renew.container")
    assert "--daemon" in renew.content_string
    assert "step certificate verify" in renew.content_string


def test_systemd_native_units(host):
    units = [
        "smallstep-cli-cleanup.timer",
        "smallstep-cli-reload.service",
        "smallstep-cli-reload.path",
    ]
    for unit in units:
        f = host.file(f"/etc/systemd/system/{unit}")
        assert f.exists
        assert f.is_file
        assert f.user == "root"
        assert f.group == "root"
        assert f.mode == 0o644

    # Specific check for reload loop
    reload_svc = host.file("/etc/systemd/system/smallstep-cli-reload.service")
    assert "systemctl reload-or-restart" in reload_svc.content_string


def test_obsolete_units_absent(host):
    obsolete = [
        "/etc/containers/systemd/smallstep-cli-init.container",
        "/etc/systemd/system/smallstep-cli-renew.timer",
    ]
    for path in obsolete:
        assert not host.file(path).exists


# def test_services_enabled(host):
#     # We only check enablement, not running state, for static verification
#     services = [
#         "smallstep-cli-renew.service",
#         "smallstep-cli-cleanup.timer",
#         "smallstep-cli-reload.path",
#     ]
#     for svc_name in services:
#         svc = host.service(svc_name)
#         assert svc.is_enabled
