from netmiko import ConnectHandler

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

def create_vlans():
    for name, dev in devices.items():
        if name == 'R2-REMOTO':
            break;  # solo SW1, SW2 y R1

        print(f"Conectando a {name} ({dev['host']})...")
        connection = ConnectHandler(**dev)

        # --- Cisco SW1 ---
        if dev['device_type'] == 'cisco_ios':
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
                    print(f"VLAN {vlan['VLAN_ID']} creada en {name}.")
                else:
                    print(f"VLAN {vlan['VLAN_ID']} ya existe en {name}.")

        # --- Mikrotik R1 ---
        elif dev['device_type'] == 'mikrotik_routeros':
            for vlan in vlans:
                vlan_name = vlan['VLAN_NAME']
                vlan_id = vlan['VLAN_ID']
                gateway = vlan['VLAN_GATEWAY']

                # Crear VLAN solo si no existe
                cmd_vlan = f""":if ([find name={vlan_name}]="") do={{ /interface vlan add name={vlan_name} vlan-id={vlan_id} interface=ether2 }}"""
                cmd_int = f""":if ([find name={vlan_name}]="") do={{/ip address add address={gateway} interface={vlan_name} }}"""

                # connection.send_command_timing(cmd_vlan)
                # connection.send_command_timing(cmd_int)
                # print(f"VLAN/INTERFAZ {vlan_id} creada en {name}.")
                output = connection.send_command_timing(f"/interface vlan print where name={vlan_name}")
                if vlan_name in output:
                    print(f"VLAN {vlan_id} ya existía en {name}.")
                else:
                    connection.send_command_timing(cmd_vlan)
                    print(f"VLAN {vlan_id} creada en {name}.")
                
                output_address = connection.send_command_timing(f"/ip address print where interface={vlan_name}")
                if vlan_name in output_address:
                    print(f'Dirección IP ya configurada en {name} para {vlan_name}.')
                else:
                    connection.send_command_timing(cmd_int)
                    print(f'Dirección IP {gateway} configurada en {name} para {vlan_name}')
        connection.disconnect()

def firewall_rules():
    dev = devices['R1-LOCAL']
    name = 'R1-LOCAL'

def test_connections():
    """Probar SSH con todos los dispositivos"""
    for name, dev in devices.items():
        try:
            conn = ConnectHandler(**dev)
            print(f"[OK] Conectado a {name} ({dev['ip']})")
            conn.disconnect()
        except Exception as e:
            print(f"[ERROR] No se pudo conectar a {name} ({dev['ip']}) -> {e}")

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
                settings_menu()
                break
            case '0':
                print("Saliendo...")    
                break
            case _:
                print("Opción inválida.")
      

if __name__ == "__main__":
    main_menu()


