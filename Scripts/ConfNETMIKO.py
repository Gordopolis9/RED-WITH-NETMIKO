from netmiko import ConnectHandler
import ipaddress
import os

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
            {'VLAN_NAME' : 'VLAN_GESTION', 'VLAN_ID' : 1799, 'VLAN_Address' : "10.10.17.56/29" },
            {'VLAN_NAME' : 'VLAN_NATIVA', 'VLAN_ID': 289}
        ]

def create_SW_vlans(connection,name):
  
    for vlan in vlans:
        # Comprobar si la VLAN ya existe
        if vlan['VLAN_NAME'] == 'VLAN_GESTION':
            continue
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
    trunk_port = 'e0/0'
    
    commands = [
        f"interface {trunk_port}",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        f"switchport trunk allowed vlan {vlans_ids['VLAN_GESTION']},{vlans_ids['VLAN_TECNICA']},{vlans_ids['VLAN_VENTAS']},{vlans_ids['VLAN_VISITANTES']}",
        f"switchport trunk native vlan {vlans_ids['VLAN_NATIVA']}",
        "duplex full",
        "no shutdown"
        
    ]
    connection.send_config_set(commands)
    connection.save_config()
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
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        f"switchport trunk allowed vlan {vlans_ids['VLAN_GESTION']},{vlans_ids['VLAN_TECNICA']},{vlans_ids['VLAN_VENTAS']},{vlans_ids['VLAN_VISITANTES']}",
        f"switchport trunk native vlan {vlans_ids['VLAN_NATIVA']}",
        "duplex full",
        "no shutdown"
        
    ]
    connection.send_config_set(commands)
    connection.save_config()
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
            if vlan_name == 'VLAN_NATIVA':
                cmd_vlan = f"/interface vlan add name={vlan_name} vlan-id={vlan_id} interface=ether2"

                output = connection.send_command(f"/interface vlan print where name={vlan_name}")
                if vlan_name in output:
                    print(f"VLAN {vlan_id} ya existía en {name}.")
                else:
                    connection.send_config_set([cmd_vlan])
                    print(f"VLAN {vlan_id} creada en {name}.")
                continue
            gateway = vlan['VLAN_GATEWAY'] if 'VLAN_GATEWAY' in vlan else vlan['VLAN_Address']
            if vlan_name == 'VLAN_GESTION':
                continue
           

            # Crear VLAN solo si no existe
            cmd_vlan = f"/interface vlan add name={vlan_name} vlan-id={vlan_id} interface=ether2"
            cmd_int = f"/ip address add address={gateway} interface={vlan_name}"

            output = connection.send_command(f"/interface vlan print where name={vlan_name}")
            if vlan_name in output:
                print(f"VLAN {vlan_id} ya existía en {name}.")
            else:
                connection.send_config_set([cmd_vlan])
                print(f"VLAN {vlan_id} creada en {name}.")
            
            output_address = connection.send_command(f"/ip address print where interface={vlan_name}")
            if vlan_name in output_address:
                print(f"Dirección IP ya configurada en {name} para {vlan_name}.")
            else:
                connection.send_config_set([cmd_int])
                print(f"Dirección IP {gateway} configurada en {name} para {vlan_name}")
    
    def firewall_rules():
        
        for vlan in vlans:
            vlan_name = vlan['VLAN_NAME']
            if vlan_name == 'VLAN_NATIVA':
                continue
            gateway = vlan['VLAN_GATEWAY'] if 'VLAN_GATEWAY' in vlan else vlan['VLAN_Address']
            if vlan_name == 'VLAN_VENTAS' or vlan_name == 'VLAN_TECNICA':
                continue
            address = ipaddress.ip_network(gateway,strict=False)
            output_filter = connection.send_command(f"/ip firewall filter print where src-address={address}")       
            if  str(address) in output_filter:
                print(f"Regla de firewall ya existe en {name} para {address}")
            else:
                cmd_firewall = f'/ip firewall filter add chain=forward src-address={address} action=drop comment="Bloqueo conexión al exterior para {vlan_name}"'
                connection.send_command(cmd_firewall)
                print(f"Regla de firewall creada en {name} para {address}")
    
    def dhcp_server():
        for vlan in vlans:
            vlan_name = vlan['VLAN_NAME']
            if vlan_name == 'VLAN_NATIVA':
                continue
            gateway = vlan['VLAN_GATEWAY'] if 'VLAN_GATEWAY' in vlan else vlan['VLAN_Address']
            if vlan_name == 'VLAN_VISITANTES':
                address = ipaddress.ip_network(gateway,strict=False)
                dhcp_name = f"DHCP_{vlan_name}"

                output_dhcp = connection.send_command(f"/ip dhcp-server print where name={dhcp_name}")
                if dhcp_name in output_dhcp:
                    print(f"Servicio de DHCP existente en {name} para {vlan_name}")
                else:
                    hosts = list(address.hosts())
                    cmd_dhcp = [
                        f"/ip pool add name=POOL_{vlan_name} ranges={hosts[1]}-{hosts[-1]}",
                        f"/ip dhcp-server add name={dhcp_name} interface={vlan_name} address-pool=POOL_{vlan_name}",
                        f"/ip dhcp-server network add address={address} gateway={hosts[0]} dns-server=8.8.8.8"
                    ]
                    connection.send_config_set(cmd_dhcp)
                    print(f"Servicio de DHCP creado para {name} en {vlan_name}")
    create_vlans()
    firewall_rules()
    dhcp_server()
    connection.disconnect()

def test_connections():
    """Probar SSH con todos los dispositivos"""
    os.system('clear')
    print('\n<-- Test conexiones SSH -->')
    for name, dev in devices.items():
        try:
            conn = ConnectHandler(**dev)
            print(f"[OK] Conexión a {name} ({dev['host']})")
            conn.disconnect()
        except Exception as e:
            print(f"[ERROR] No se pudo conectar a {name} ({dev['host']}) -> {e}")
    input('\nPresione Enter para continuar...')


def configure_network():
    # configurar la red
    os.system('clear')
    while True:
        
        print('\n<-- Configuración automática de red -->')
        print('1. Ver configuracion preestablecida')
        print('2. Iniciar configuración automática')
        print('3. Eliminar configuración existente')
        print('0. Volver al menú principal')

        choice = input('Seleccione una opción: ')

        match choice:
            case '1':
                os.system('clear')
                print('\n<-- Configuración Preestablecida -->')
                print('\n🔗 Vlans')
                for vlan in vlans:
                    print(f"| VLAN: {vlan['VLAN_NAME']}, ID: {vlan['VLAN_ID']}, Gateway: {vlan['VLAN_GATEWAY'] if 'VLAN_GATEWAY' in vlan else vlan['VLAN_Address']}")
                print('\n Dispositivos:')
                for name,dev in devices.items():
                    print(f"| {name} ({dev['device_type']}) - {dev['host']} - username: {dev['username']}, password: {dev['password']}, secret/port: {dev['secret'] if 'secret' in dev else dev['port']}")
                input('\nPresione Enter para continuar...')
                os.system('clear')
            case '2':
                os.system('clear')
                print('\n🔧 Iniciando configuración automática de red...')
                sw1_local()
                sw2_remoto()
                r1_local()
                print('\n✅ Configuración automática completada.')
                input('\nPresione Enter para continuar...')
                os.system('clear')
            case '3':
                print('\n🧹 Eliminando configuración existente... (No Implementado)')
                # Aquí se implementara la logica para eliminar la configuracion existente de la red 
            case '0':
                os.system('clear')
                break
            case _:
                os.system('clear')
                print('Opción inválida, intente nuevamente.')
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
        'cisco_ios': [
            ('show ip interface brief', "Interfaces"),
            ('show vlan brief', "VLANs")
        ],
        'mikrotik_routeros': [
            ('/interface print', "Interfaces"),
            ('/ip address print', "Direcciones IP"),
            ('/ip firewall filter print', "Reglas de Firewall"),
            ('/ip dhcp-server print', "DHCP Server"),
            ('/ip route print', "Tabla de Rutas")
        ]
    }

    while True:
        os.system('clear')
        choice = menu_dispositivos()
        if choice == '0':
            print("Saliendo...")
            break
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(devices):
            print("Opción inválida, intente nuevamente.")
            continue

        name = list(devices.keys())[int(choice) - 1]
        dev = devices[name]
        os.system('clear')
        print(f"\n🔗 Conectando a {name} ({dev['host']})...")
        connection = ConnectHandler(**dev)
        if dev['device_type'] == 'cisco_ios':
            connection.enable()

        print(f"\n📡 Configuración de {name}:\n")
        for cmd, titulo in commands[dev['device_type']]:
            print(f"\n<-- {titulo} ({cmd}) -->")
            output = connection.send_command(cmd)
            print(output)

        connection.disconnect()
        input('\nPresione Enter para continuar...')


def settings_menu():
    # --> Menu de configuraciones -->  
    os.system('clear')
    def update_device(devices, device_name, key, new_value):
        if device_name in devices and key in devices[device_name]:
            devices[device_name][key] = new_value
            print(f"✅ {device_name} -> {key} actualizado a: {new_value}")
        else:
            print(f"⚠️ No se encontró {device_name} o la clave {key}")
    
    def update_vlan(vlan, key, new_value):
        vlan[key] = new_value
        print(f"✅ {vlan['VLAN_NAME']} -> {key} actualizado a: {new_value}")

    while True:
        print('\n<-- Ajustes -->')
        print('1. Configurar dispositivos')
        print('2. Configurar VLANs')
        print('0. Volver')

        choice = input('Seleccione una opción: ')

        match choice:
            case '1':
                os.system('clear')
                print('\n<-- Cinfigurar Dispositivos -->')
                opcion_dispositivo = menu_dispositivos()
                if opcion_dispositivo == '0':
                    print("Saliendo...")
                    break
                if not opcion_dispositivo.isdigit() or int(opcion_dispositivo) < 1 or int(opcion_dispositivo) > len(devices):
                    print("Opción inválida, intente nuevamente.")
                    continue 
                
                name = list(devices.keys())[int(opcion_dispositivo) - 1]
                dev = devices[name]
                os.system('clear')
                while True: 
                    print(f"\n<-- Configuración de {name} -->")   
                    print('1. Host (IP de gestión)')
                    print('2. Username (Usuario)')
                    print('3. Password (Contraseña)')
                    if dev['device_type'] == 'cisco_ios':
                        print('4. Secret (Cisco_IOS)')
                    else:
                        print('4. Port (MikroTik_RouterOS)')
                    print('0. Volver')

                    choice = input('Seleccione una opción: ')

                    match choice:
                        case '1':
                            os.system('clear')
                            new_host = input(f"Ingrese nuevo Host (IP de gestión) para {name} (actual: {dev['host']}): ")
                            old_host = dev['host']
                            update_device(devices, name, 'host', new_host)
                          
                            input('\nPresione Enter para continuar...')
                            os.system('clear')
                        case '2':
                            os.system('clear')
                            new_username = input(f"Ingrese nuevo Username (Usuario) para {name} (actual: {dev['username']}): ")
                            old_username = dev['username']
                            update_device(devices, name, 'username', new_username)
                            
                            input('\nPresione Enter para continuar...')
                            os.system('clear')
                        case '3':
                            os.system('clear')
                            new_password = input(f"Ingrese nuevo Password (Contraseña) para {name} (actual: {dev['password']}): ")
                            old_password = dev['password']
                            update_device(devices, name, 'password', new_password)
                           
                            input('\nPresione Enter para continuar...')
                            os.system('clear')
                        case '4':
                            if dev['device_type'] == 'cisco_ios':
                                os.system('clear')
                                new_secret = input(f"Ingrese nuevo Secret para {name} (actual: {dev['secret']}): ")
                                old_secret = dev['secret']
                                update_device(devices, name, 'secret', new_secret)
                               
                                input('\nPresione Enter para continuar...')
                                os.system('clear')
                            else:
                                os.system('clear')
                                new_port = input(f"Ingrese nuevo Port para {name} (actual: {dev['port']}): ")
                                old_port = dev['port']
                                update_device(devices, name, 'port', new_port)
                                
                                input('\nPresione Enter para continuar...')
                                os.system('clear')
                        case '0':
                            os.system('clear')
                            break
                        case _:
                            os.system('clear')
                            print('Opción inválida, intente nuevamente.')
            case '2':
                os.system('clear')
                def menu_vlans():
                    print('\n Seleccione una VLAN para configurar: ')
                    for idx, vlan in enumerate(vlans, 1):
                        print(f"{idx}. {vlan['VLAN_NAME']} (ID: {vlan['VLAN_ID']})")
                    print('0. Volver')
                    choice = input('Seleccione una opción: ')
                    return choice
                choice_vlan = menu_vlans()

                if choice_vlan == '0':
                    print("Saliendo...")
                    break
                if not choice_vlan.isdigit() or int(choice_vlan) < 1 or int(choice_vlan) > len(vlans):
                    print("Opción inválida, intente nuevamente.")
                    continue 

                vlan = vlans[int(choice_vlan) - 1]
                os.system('clear')
                while True:
                    print(f"\n<-- Configuración de {vlan['VLAN_NAME']} -->")
                    print('1. VLAN ID')
                    if vlan['VLAN_NAME'] == 'VLAN_GESTION':
                        print('2. VLAN Address')
                    else:
                        print('2. VLAN Address')
                    print('0. Volver')

                    choice = input('Seleccione una opción: ')

                    match choice:
                        case '1':
                            os.system('clear')
                            new_vlan_id = input(f"Ingrese nuevo VLAN ID para {vlan['VLAN_NAME']} (actual: {vlan['VLAN_ID']}): ")
                            old_vlan_id = vlan['VLAN_ID']
                            update_vlan(vlan, 'VLAN_ID', new_vlan_id)
                            print(f"VLAN ID actualizado: {old_vlan_id} -> {new_vlan_id}")
                            input('\nPresione Enter para continuar...')
                            os.system('clear')
                        case '2':
                            if vlan['VLAN_NAME'] == 'VLAN_GESTION':
                                os.system('clear')
                                new_vlan_address = input(f"Ingrese nueva VLAN Address para {vlan['VLAN_NAME']} (actual: {vlan.get('VLAN_Address', 'No configurado')}): ")
                                old_vlan_address = vlan.get('VLAN_Address', 'No configurado')
                                update_vlan(vlan, 'VLAN_Address', new_vlan_address)
                                print(f"VLAN Address actualizado: {old_vlan_address} -> {new_vlan_address}")
                                input('\nPresione Enter para continuar...')
                                os.system('clear')
                            else:
                                os.system('clear')
                                new_vlan_gateway = input(f"Ingrese nuevo VLAN Gateway para {vlan['VLAN_NAME']} (actual: {vlan['VLAN_GATEWAY']}): ")
                                old_vlan_gateway = vlan['VLAN_GATEWAY']
                                update_vlan(vlan, 'VLAN_GATEWAY', new_vlan_gateway)
                                print(f"VLAN Gateway actualizado: {old_vlan_gateway} -> {new_vlan_gateway}")
                                input('\nPresione Enter para continuar...')
                                os.system('clear')
                        case '0':
                            os.system('clear')
                            break
                        case _:
                            os.system('clear')
                            print('Opción inválida, intente nuevamente.')
            case '0':
                os.system('clear')
                break
            case _:
                os.system('clear')
                print('Opción inválida, intente nuevamente.')
        

   

def main_menu():
    
    while True:
        os.system('clear')
        print("\n<-- MENU PRINCIPAL -->")
        print("1. Testear conexiones SSH")
        print("2. Mostrar configuraciones")
        print("3. Configurar red (Automatico)")
        print("4. Ajustes (Settings)")
        print("0. Salir")
        
        choice = input("Seleccione una opción: ")
        
        match choice:
            case '1':
                test_connections()
            case '2':
                show_config()
            case '3':
                configure_network()
            case '4':
                settings_menu()
            case '0':
                print("Saliendo...")    
                break
            case _:
                print("Opción inválida.")
      

if __name__ == "__main__":
    main_menu()


