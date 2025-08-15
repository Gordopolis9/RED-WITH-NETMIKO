from netmiko import ConnectHandler

# routers_mikrotik = [
#     {
#         # Router LOCAL
#         'name' : 'local_route',
#         'device_type': 'mikrotik_routeros',
#         'host': 'COLOCAR IP',
#         'username' : 'admin',
#         'password' : 'admin',
#         'port' : 22,
#         'secret' : '',
#         'local_config' :{
#             'vlans' : [
#             {'VLAN_NAME' : 'VLAN_VENTAS', 'VLAN_ID' : 280, 'VLAN_GATEWAY' : "10.10.17.1/27" },
#             {'VLAN_NAME' : 'VLAN_TECNICA', 'VLAN_ID' : 281, 'VLAN_GATEWAY' : "10.10.17.33/28" },
#             {'VLAN_NAME' : 'VLAN_VISITANTES', 'VLAN_ID' : 282, 'VLAN_GATEWAY' : "10.10.17.49/29" },
#             {'VLAN_NAME' : 'VLAN_GESTION', 'VLAN_ID' : 1799, 'VLAN_GATEWAY' : "10.10.17.57/29" }
#             ],
#             'interface' : 'ether2',
#         },
#         'external_config' : {
#             'interface' : 'ether3',
#             'ip' : '10.10.17.65/30',
#             'next_hop' : '10.10.17.66'
#         }
        

#     }
# ]

devices = [
    {
        'name': 'SW1-LOCAL',
        'device_type': 'cisco_ios',
        'host': '10.10.17.58',  # IP de gestión del SW1
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin'
    },
    {
        'name': 'SW2-REMOTO',
        'device_type': 'cisco_ios',
        'host': '10.10.17.61',  # IP de gestión del SW2
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin'
    },
    {
        'name': 'R1-LOCAL',
        'device_type': 'mikrotik_routeros',
        'host': '10.10.17.59',  # IP de gestión del R1
        'username': 'admin',
        'password': 'admin',
        'port': 22
    },
    {
        'name': 'R2-REMOTO',
        'device_type': 'mikrotik_routeros',
        'host': '10.10.17.60',  # IP de gestión del R2
        'username': 'admin',
        'password': 'admin',
        'port': 22
    }
]

vlans = [
            {'VLAN_NAME' : 'VLAN_VENTAS', 'VLAN_ID' : 280, 'VLAN_GATEWAY' : "10.10.17.1/27" },
            {'VLAN_NAME' : 'VLAN_TECNICA', 'VLAN_ID' : 281, 'VLAN_GATEWAY' : "10.10.17.33/28" },
            {'VLAN_NAME' : 'VLAN_VISITANTES', 'VLAN_ID' : 282, 'VLAN_GATEWAY' : "10.10.17.49/29" },
            {'VLAN_NAME' : 'VLAN_GESTION', 'VLAN_ID' : 1799, 'VLAN_GATEWAY' : "10.10.17.57/29" }
        ]

def create_vlans():
    for device in devices:
        if device['name'] not in ['SW1-LOCAL', 'R1-LOCAL']:
            continue  # solo SW1 y R1

        print(f"Conectando a {device['name']} ({device['host']})...")
        connection = ConnectHandler(**device)

        # --- Cisco SW1 ---
        if device['device_type'] == 'cisco_ios':
            connection.enable()
            for vlan in vlans:
                # Comprobar si la VLAN ya existe
                output = connection.send_command(f"show vlan brief | include {vlan['VLAN_ID']}")
                if str(vlan['VLAN_ID']) not in output:
                    commands = [
                        f"vlan {vlan['VLAN_ID']}",
                        f"name {vlan['VLAN_NAME']}"
                    ]
                    connection.send_config_set(commands)
                    print(f"VLAN {vlan['VLAN_ID']} creada en {device['name']}.")
                else:
                    print(f"VLAN {vlan['VLAN_ID']} ya existe en {device['name']}.")

        # --- Mikrotik R1 ---
        elif device['device_type'] == 'mikrotik_routeros':
            for vlan in vlans:
                vlan_name = vlan['VLAN_NAME']
                vlan_id = vlan['VLAN_ID']
                gateway = vlan['VLAN_GATEWAY']

                # Crear VLAN solo si no existe
                cmd_vlan = f""":if ([find name={vlan_name}]="") do={{ /interface vlan add name={vlan_name} vlan-id={vlan_id} interface=ether2 }}"""
                cmd_int = f""":if ([find name={vlan_name}]="") do={{/ip address add address={gateway} interface={vlan_name} }}"""

                # connection.send_command_timing(cmd_vlan)
                # connection.send_command_timing(cmd_int)
                # print(f"VLAN/INTERFAZ {vlan_id} creada en {device['name']}.")
                output = connection.send_command_timing(f"/interface vlan print where name={vlan_name}")
                if vlan_name in output:
                    print(f"VLAN {vlan_id} ya existía en {device['name']}.")
                else:
                    connection.send_command_timing(cmd_vlan)
                    print(f"VLAN {vlan_id} creada en {device['name']}.")
                
                output_address = connection.send_command_timing(f"/ip address print where interface={vlan_name}")
                if vlan_name in output_address:
                    print(f'Dirección IP ya configurada en {device['name']} para {vlan_name}.')
                else:
                    connection.send_command_timing(cmd_int)
                    print(f'Dirección IP {gateway} configurada en {device['name']} para {vlan_name}')
        connection.disconnect()

create_vlans()
