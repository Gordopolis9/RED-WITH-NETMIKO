from netmiko import ConnectHandler

# Lista de dispositivos
devices = [
    {
        'name': 'SW1-LOCAL',
        'device_type': 'cisco_ios',
        'host': '10.10.17.58',
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin'
    },
    {
        'name': 'SW2-REMOTO',
        'device_type': 'cisco_ios',
        'host': '10.10.17.61',
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin'
    },
    {
        'name': 'R1-LOCAL',
        'device_type': 'mikrotik_routeros',
        'host': '10.10.17.59',
        'username': 'admin',
        'password': 'admin',
        'port': 22
    },
    {
        'name': 'R2-REMOTO',
        'device_type': 'mikrotik_routeros',
        'host': '10.10.17.60',
        'username': 'admin',
        'password': 'admin',
        'port': 22
    }
]

# Comandos por tipo de dispositivo
commands = {
    'cisco_ios': 'show ip interface brief',
    'mikrotik_routeros': '/ip address print'
}

def menu_dispositivos():
    print("\nSeleccione un dispositivo para conectarse:")
    for idx, device in enumerate(devices, 1):
        print(f"{idx}. {device['name']} ({device['host']})")
    print("0. Salir")
    choice = input("Ingrese el número: ")
    return choice

def main():
    while True:
        choice = menu_dispositivos()
        if choice == '0':
            print("Saliendo...")
            break
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(devices):
            print("Opción inválida, intente nuevamente.")
            continue

        device = devices[int(choice) - 1]
        print(f"\n🔗 Conectando a {device['name']} ({device['host']})...")
        net_connect = ConnectHandler(**device)
        if device['device_type'] == 'cisco_ios':
            net_connect.enable()
        output = net_connect.send_command(commands[device['device_type']])
        print(f"📡 Salida de {device['name']}:\n{output}")
        net_connect.disconnect()

if __name__ == "__main__":
    main()
