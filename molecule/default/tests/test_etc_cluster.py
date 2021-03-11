import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('etcd_cluster')

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