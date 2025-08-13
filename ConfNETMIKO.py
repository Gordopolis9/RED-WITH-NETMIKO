from netmiko import ConnectHandler

routers_mikrotik = [
    {
        # Router LOCAL
        'name' : 'local_route',
        'device_type': 'mikrotik_routeros',
        'host': 'COLOCAR IP',
        'username' : 'admin',
        'password' : 'admin',
        'port' : 22,
        'secret' : '',
        'local_config' :{
            'vlans' : [
            {'VLAN_NAME' : 'VLAN_VENTAS', 'VLAN_ID' : 280, 'VLAN_GATEWAY' : "10.10.17.1/27" },
            {'VLAN_NAME' : 'VLAN_TECNICA', 'VLAN_ID' : 281, 'VLAN_GATEWAY' : "10.10.17.33/28" },
            {'VLAN_NAME' : 'VLAN_VISITANTES', 'VLAN_ID' : 282, 'VLAN_GATEWAY' : "10.10.17.49/29" },
            {'VLAN_NAME' : 'VLAN_GESTION', 'VLAN_ID' : 1799, 'VLAN_GATEWAY' : "10.10.17.57/29" }
            ],
            'interface' : 'ether2',
        },
        'external_config' : {
            'interface' : 'ether3',
            'ip' : '10.10.17.65/30',
            'next_hop' : '10.10.17.66'
        }
        

    }
]