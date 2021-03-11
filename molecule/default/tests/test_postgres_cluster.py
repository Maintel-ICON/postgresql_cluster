import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('postgres_cluster')

@pytest.fixture(scope='module')
def hostname(host):
    return host.ansible.get_variables()['inventory_hostname']

def test_hostname(host, hostname):
    assert host.check_output('hostname -s') != hostname

def test_etc_hosts_has_our_name(host, hostname):
    assert(
        hostname.lower() in
        host.file('/etc/hosts').content_string.lower()
    )
def test_sudo(host):
    with host.sudo():
        assert host.check_output('whoami') == 'root'


@pytest.mark.parametrize('pkg', [
    'postgresql-12',
    'postgresql-client-12',
    'postgresql-server-dev-12',
    'iptables'
])
def test_pkg(host, pkg):
    package = host.package(pkg)

    assert package.is_installed

@pytest.mark.parametrize('svc', [
    'pgbouncer'
])
def test_svc(host, svc):
    service = host.service(svc)

    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize('port', [
    8008,
    5432,
    6432
])
def test_ports(host, hostname, port):
    socket = host.socket("tcp://%s:%s" % (hostname,port))

    assert socket.is_listening
