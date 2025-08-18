from netmiko import ConnectHandler
import ipaddress

devices = {
    'SW1-LOCAL':{
        'device_type': 'cisco_ios',
        'host': '10.10.17.58',  # IP de gestión del SW1
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin'
    },
    'SW2-REMOTO':{
        'device_type': 'cisco_ios',
        'host': '10.10.17.61',  # IP de gestión del SW2
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin'
    },
    'R1-LOCAL':{
        'device_type': 'mikrotik_routeros',
        'host': '10.10.17.59',  # IP de gestión del R1
        'username': 'admin',
        'password': 'admin',
        'port': 22
    },
    'R2-REMOTO':{
        'device_type': 'mikrotik_routeros',
        'host': '10.10.17.60',  # IP de gestión del R2
        'username': 'admin',
        'password': 'admin',
        'port': 22
    }
}

vlans = [
            {'VLAN_NAME' : 'VLAN_VENTAS', 'VLAN_ID' : 280, 'VLAN_GATEWAY' : "10.10.17.1/27" },
            {'VLAN_NAME' : 'VLAN_TECNICA', 'VLAN_ID' : 281, 'VLAN_GATEWAY' : "10.10.17.33/28" },
            {'VLAN_NAME' : 'VLAN_VISITANTES', 'VLAN_ID' : 282, 'VLAN_GATEWAY' : "10.10.17.49/29" },
            {'VLAN_NAME' : 'VLAN_GESTION', 'VLAN_ID' : 1799, 'VLAN_GATEWAY' : "10.10.17.57/29" }
        ]

def create_SW_vlans(connection,name):
  
    for vlan in vlans:
        # Comprobar si la VLAN ya existe
        output = connection.send_command(f"show vlan brief | include {vlan['VLAN_ID']}")
        if str(vlan['VLAN_ID']) not in output:
            commands = [
                f"vlan {vlan['VLAN_ID']}",
                f"name {vlan['VLAN_NAME']}"
            ]
            connection.send_config_set(commands)
            print(f"VLAN {vlan['VLAN_ID']} creada en {name}.")
        else:
            print(f"VLAN {vlan['VLAN_ID']} ya existe en {name}.")

def sw1_local():
    dev = devices['SW1-LOCAL']
    name = 'SW1-LOCAL'
    vlans_ids = {vlan['VLAN_NAME']:vlan['VLAN_ID']for vlan in vlans}
    print(f"\n🔗 Conectando a {name} ({dev['host']})...")
    connection = ConnectHandler(**dev)
    connection.enable()

    create_SW_vlans(connection,name)

    # Configurar puertos de acceso
    access_ports = {
        'e0/1': vlans_ids['VLAN_VENTAS'],  # Puerto para VLAN_VENTAS
        'e0/2': vlans_ids['VLAN_TECNICA'],  # Puerto para VLAN_TECNICA
        'e0/3': vlans_ids['VLAN_VISITANTES']   # Puerto para VLAN_VISITANTES
    }

    for port, vlan_id in access_ports.items():
        commands = [
            f"interface {port}",
            "switchport mode access",
            f"switchport access vlan {vlan_id}",
            "no shutdown"
        ]
        connection.send_config_set(commands)
        print(f"Puerto {port} configurado para VLAN {vlan_id} en {name}.")

    # Configurar puerto troncal
    trunk_port = 'e1/0'
    
    commands = [
        f"interface {trunk_port}",
        "switchport mode trunk",
        f"switchport trunk allowed vlan {vlans_ids['VLAN_GESTION']},{vlans_ids['VLAN_TECNICA']},{vlans_ids['VLAN_VENTAS']},{vlans_ids['VLAN_VISITANTES']}",
        "no shutdown",
        "do wr"
    ]
    connection.send_config_set(commands)
    print(f"Puerto {trunk_port} configurado como troncal en {name}.")

    connection.disconnect()

def sw2_remoto():
    dev = devices['SW2-REMOTO']
    name = 'SW2-REMOTO'
    vlans_ids = {vlan['VLAN_NAME']:vlan['VLAN_ID']for vlan in vlans}
    print(f"\n🔗 Conectando a {name} ({dev['host']})...")
    connection = ConnectHandler(**dev)
    connection.enable()

    create_SW_vlans(connection,name)

    # Configurar puertos de acceso

    # access_ports = {
    #     'e0/1': vlans_ids['VLAN_VENTAS'],  # Puerto para VLAN_VENTAS
    #     'e0/2': vlans_ids['VLAN_TECNICA'],  # Puerto para VLAN_TECNICA
    #     'e0/3': vlans_ids['VLAN_VISITANTES']   # Puerto para VLAN_VISITANTES
    # }

    # for port, vlan_id in access_ports.items():
    #     commands = [
    #         f"interface {port}",
    #         "switchport mode access",
    #         f"switchport access vlan {vlan_id}",
    #         "no shutdown"
    #     ]
    #     connection.send_config_set(commands)
    #     print(f"Puerto {port} configurado para VLAN {vlan_id} en {name}.")

    # Configurar puerto troncal
    trunk_port = 'e0/0'
    
    commands = [
        f"interface {trunk_port}",
        "switchport mode trunk",
        f"switchport trunk allowed vlan {vlans_ids['VLAN_GESTION']},{vlans_ids['VLAN_TECNICA']},{vlans_ids['VLAN_VENTAS']},{vlans_ids['VLAN_VISITANTES']}",
        "no shutdown",
        "do wr"
    ]
    connection.send_config_set(commands)
    print(f"Puerto {trunk_port} configurado como troncal en {name}.")

    connection.disconnect()
def r1_local():
    dev = devices['R1-LOCAL']
    name = 'R1-LOCAL'

    print(f"\n🔗 Conectando a {name} ({dev['host']})...")
    connection = ConnectHandler(**dev)

    def create_vlans():
        for vlan in vlans:
            vlan_name = vlan['VLAN_NAME']
            vlan_id = vlan['VLAN_ID']
            gateway = vlan['VLAN_GATEWAY']
            if vlan_name != 'VLAN_GESTION':
                continue
           

            # Crear VLAN solo si no existe
            cmd_vlan = f'/interface vlan add name={vlan_name} vlan-id={vlan_id} interface=ether2'
            cmd_int = f'/ip address add address={gateway} interface={vlan_name}'

            output = connection.send_command(f"/interface vlan print where name={vlan_name}")
            if vlan_name in output:
                print(f"VLAN {vlan_id} ya existía en {name}.")
            else:
                connection.send_config_set(cmd_vlan)
                print(f"VLAN {vlan_id} creada en {name}.")
            
            output_address = connection.send_command(f"/ip address print where interface={vlan_name}")
            if vlan_name in output_address:
                print(f'Dirección IP ya configurada en {name} para {vlan_name}.')
            else:
                connection.send_config_set(cmd_int)
                print(f'Dirección IP {gateway} configurada en {name} para {vlan_name}')
    
    def firewall_rules():
        
        for vlan in vlans:
            vlan_name = vlan['VLAN_NAME']
            gateway = vlan['VLAN_GATEWAY']
            if vlan_name == 'VLAN_GESTION' or vlan_name == 'VLAN_VISITANTES':
                continue
            address = ipaddress.ip_network(gateway,strict=False)
            output_filter = connection.send_command(f'/ip firewall filter print where src-address={address}')       
            if  str(address) in output_filter:
                print(f'Regla de firewall ya existe en {name} para {address}')
            else:
                cmd_firewall = f'/ip firewall filter add chain=forward src-address={address} action=drop comment="Bloqueo conexión al exterior para {vlan_name}"'
                connection.send_config_set(cmd_firewall)
                print(f'Regla de firewall creada en {name} para {address}')
    
    def dhcp_server():
        for vlan in vlans:
            vlan_name = vlan['VLAN_NAME']
            gateway = vlan['VLAN_GATEWAY']
            if vlan_name == 'VLAN_VISITANTES':
                address = ipaddress.ip_network(gateway,strict=False)
                dhcp_name = f'DHCP_{vlan_name}'

                output_dhcp = connection.send_command(f'/ip dhcp-server print where name={dhcp_name}')
                if dhcp_name in output_dhcp:
                    print(f'Servicio de DHCP existente en {name} para {vlan_name}')
                else:
                    hosts = list(address.hosts())
                    cmd_dhcp = [
                        f'/ip pool add name=POOL_{vlan_name} ranges={hosts[1]}-{hosts[-1]}',
                        f'/ip dhcp-server add name={dhcp_name} interface={vlan_name} address-pool=POOL_{vlan_name}',
                        f'/ip dhcp-server network add address={address} gateway={hosts[0]} dns-server=8.8.8.8'
                    ]
                    connection.send_config_set(cmd_dhcp)
                    print(f'Servicio de DHCP creado para {name} en {vlan_name}')
    create_vlans()
    firewall_rules()
    dhcp_server()
    connection.disconnect()

def test_connections():
    """Probar SSH con todos los dispositivos"""
    for name, dev in devices.items():
        try:
            conn = ConnectHandler(**dev)
            print(f"[OK] Conectado a {name} ({dev['host']})")
            conn.disconnect()
        except Exception as e:
            print(f"[ERROR] No se pudo conectar a {name} ({dev['host']}) -> {e}")

def configure_network():
    # configurar la red
    sw1_local()
    sw2_remoto()
    r1_local()
    # r2_remoto() # Implementar si es necesario

def menu_dispositivos():
    """Mostrar menú de dispositivos y devolver la selección"""
    print("\nSeleccione un dispositivo para conectarse:")
    for idx, (name, dev) in enumerate(devices.items(), 1):
        print(f"{idx}. {name} ({dev['host']})")
    print("0. Volver")
    
    choice = input("Ingrese el número: ")
    return choice
    


def show_config():
    # mostrar configuraciones de RED
    commands = {
        'cisco_ios': ['show ip interface brief', 'show vlan brief'],
        'mikrotik_routeros': ['/interface print', '/ip address print', '/ip firewall filter print','/ip dhcp-server print','/ip route print']
    }
    while True:
        choice = menu_dispositivos()
        if choice == '0':
            print("Saliendo...")
            break
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(devices):
            print("Opción inválida, intente nuevamente.")
            continue

       
        name = list(devices.keys())[int(choice) - 1]
        dev = devices[name]

        print(f"\n🔗 Conectando a {name} ({dev['host']})...")
        connection = ConnectHandler(**dev)
        if dev['device_type'] == 'cisco_ios':
            connection.enable()
        print(f"📡 Salida de {name}:")
        for cmd in commands[dev['device_type']]:
            output = connection.send_command(cmd)
            print(output)

        
        connection.disconnect()


def main_menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Testear conexiones SSH")
        print("2. Mostrar configuraciones")
        print("3. Configurar red")
        print("4. Settings")
        print("0. Salir")
        
        choice = input("Seleccione una opción: ")
        
        match choice:
            case '1':
                test_connections()
                break
            case '2':
                show_config()
                break
            case '3':
                configure_network()
                break
            case '4':
                #settings_menu()
                break
            case '0':
                print("Saliendo...")    
                break
            case _:
                print("Opción inválida.")
      

if __name__ == "__main__":
    main_menu()


