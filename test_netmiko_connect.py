from netmiko import ConnectHandler

# Lista de dispositivos (ajustá las IPs según tu topología)
devices = [
    {
        'device_type': 'cisco_ios',
        'host': '10.10.17.58',  # IP de gestión del SW1
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin'
    },
    {
        'device_type': 'cisco_ios',
        'host': '10.10.17.61',  # IP de gestión del SW2
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin'
    },
    {
        'device_type': 'mikrotik_routeros',
        'host': '10.10.17.59',  # IP de gestión del R1
        'username': 'admin',
        'password': 'admin',
        'port': 22
    },
    {
        'device_type': 'mikrotik_routeros',
        'host': '10.10.17.60',  # IP de gestión del R2
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

# Recorrer y conectar
for device in devices:
    print(f"\n🔗 Conectando a {device['host']} ({device['device_type']})...")
    net_connect = ConnectHandler(**device)
    if device['device_type'] == 'cisco_ios':
        net_connect.enable()
    output = net_connect.send_command(commands[device['device_type']])
    print(f"📡 Salida de {device['host']}:\n{output}")
    net_connect.disconnect()
