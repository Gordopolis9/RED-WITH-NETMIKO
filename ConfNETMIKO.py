from netmiko import ConnectHandler

routers_mikrotik = [
    {
        # Router LOCAL
        'device_type': 'mikrotik_routeros',
        'host': 'COLOCAR IP',
        'username' : 'admin',
        'password' : 'admin',
        'port' : 22,
        'secret' : '',
        'config' : {
            'ip_address-VENTAS-280' : '10.10.17.1',
            'interface-VENTAS-280' : 'VLAN_VENTAS',
            'ip_addres-external' : '10.10.17.65',
            'interface-external' : 'ether1',
        }


    }
]