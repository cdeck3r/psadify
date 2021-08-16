import os
import shutil

import pytest
from src.psadify import psadify

''' Unit tests for get_last_attacks

    In all tests: 
    * /var/log/<ip address>
    * /var/log/<ip address>/<ip address>_whois
    * /var/log/<ip address>/<ip address>_email_alert
    * /var/log/<ip address>/<ip address>_packet_ctr
    * /var/log/<ip address>/<ip address>_start_time
    * /var/log/<ip address>/<ip address>_danger_level
    * /var/log/<ip address>/<ip address>_email_ctr

'''


# redirected method, because I must be able
# to call it directly as well
def _setup(addr, psad_log_dir):
    ipaddress_str = addr
    log_dir = psad_log_dir
    os.makedirs(os.path.join(log_dir, ipaddress_str), mode=0o700)

    files = [
        ipaddress_str + '_whois',
        ipaddress_str + '_email_alert',
        ipaddress_str + '_packet_ctr',
        ipaddress_str + '_start_time',
        ipaddress_str + '_danger_level',
        ipaddress_str + '_email_ctr',
    ]
    # create files
    for f in files:
        with open(os.path.join(psad_log_dir, ipaddress_str, f), 'w') as fp:
            pass


# redirected method, because I must be able
# to call it directly as well
def _teardown(psad_log_dir):
    # teardown
    shutil.rmtree(psad_log_dir, ignore_errors=True)


# called before each test
@pytest.fixture(autouse=True)
def setup(request, ipaddress_str, psad_log_dir):
    _setup(ipaddress_str, psad_log_dir)  # redirected method

    def teardown():
        _teardown(psad_log_dir)

    request.addfinalizer(teardown)


#
# other fixtures
#
@pytest.fixture
def psad_log_dir():
    return '/var/log/psad'


@pytest.fixture
def ipaddress_str():
    return "108.13.17.25"


@pytest.fixture
def internal_ipaddress_str():
    return "192.168.100.10"


#
# unit tests start here
#
def test_internal_ip_default(internal_ipaddress_str, psad_log_dir):
    # remove dir tree created by autosense fixture and
    # call fixture with internal ip again
    shutil.rmtree(psad_log_dir, ignore_errors=True)
    _setup(internal_ipaddress_str, psad_log_dir)

    # call get_last_attacks from psadify.py
    last_attacks = psadify.get_last_attacks()
    assert last_attacks == []
    assert len(last_attacks) == 0
    # take care of teardown
    _teardown(psad_log_dir)


def test_empty_files_internal_ip_filter_disable(internal_ipaddress_str, psad_log_dir):
    # remove dir tree created by autosense fixture and
    # call fixture with internal ip again
    shutil.rmtree(psad_log_dir, ignore_errors=True)
    _setup(internal_ipaddress_str, psad_log_dir)

    # call get_last_attacks from psadify.py
    last_attacks = psadify.get_last_attacks(filter_private_ip=False)
    assert len(last_attacks) == 1
    for attacker_dict in last_attacks:
        for key, value in attacker_dict.items():
            if key in ['first_seen', 'IP', 'country', 'ports']:
                assert value == '?'

    # take care of teardown
    _teardown(psad_log_dir)


def test_empty_files():
    last_attacks = psadify.get_last_attacks()
    # print(last_attacks)
    assert len(last_attacks) == 1

    for attacker_dict in last_attacks:
        for key, value in attacker_dict.items():
            if key in ['first_seen', 'IP', 'country', 'ports']:
                assert value == '?'
