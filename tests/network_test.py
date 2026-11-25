import pytest
import sys

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="tests for linux only")

import sdbus
from sdbus_block.networkmanager import (
    ConnectionType,
    NetworkManagerSettings,
    NetworkConnectionSettings,
)



def setup_module(module):
    """setup network test module."""
    sdbus.set_default_bus(sdbus.sd_bus_open_system())

def display_network_path (path: str):
    profile = NetworkConnectionSettings(path).get_profile()
    print("-------------------------------------------------------------")
    print("name:", profile.connection.connection_id)
    print("uuid:", profile.connection.uuid)
    print("type:", profile.connection.connection_type)
    if profile.connection.interface_name:
        print("      interface-name:", profile.connection.interface_name)
    if profile.ipv4:
        print("ipv4: method:", profile.ipv4.method)
        if profile.ipv4.address_data:
            for address in profile.ipv4.address_data:
                print(f'      ipaddr: {address.address}/{address.prefix}')
        if profile.ipv4.route_metric:
            print(f'      route-metric: {profile.ipv4.route_metric}')
    if profile.ipv6:
        print("ipv6: method:", profile.ipv6.method)
    if profile.connection.connection_type == ConnectionType.WIFI:
        assert profile.wireless
        assert profile.wireless.ssid
        print("ssid:", profile.wireless.ssid.decode())

def test_list_connection_path ():
    print ('\n')

    networkmanager_settings = NetworkManagerSettings()
    for dbus_connection_path in networkmanager_settings.connections:
        print (dbus_connection_path)

    for dbus_connection_path in networkmanager_settings.connections:
        display_network_path (dbus_connection_path)

def teardown_module(module):
    """teardown network test module.
    """
