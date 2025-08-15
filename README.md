# Subneteo y Direccionamiento IPv4 - VLSM para 10.10.17.0/24

| VLAN         | Red Subnet       | Máscara          | Rango Hosts Válidos       | Dirección Broadcast | Hosts Usables | IP Gateway (Router) |
|--------------|------------------|------------------|---------------------------|---------------------|--------------|--------------------|
| Ventas (280) | 10.10.17.0/27    | 255.255.255.224  | 10.10.17.1 – 10.10.17.30  | 10.10.17.31         | 30           | 10.10.17.1         |
| Técnica (281)| 10.10.17.32/28   | 255.255.255.240  | 10.10.17.33 – 10.10.17.46 | 10.10.17.47         | 14           | 10.10.17.33        | 
| Visitantes(282)| 10.10.17.48/29 | 255.255.255.248  | 10.10.17.49 – 10.10.17.54 | 10.10.17.55         | 6            | 10.10.17.49        | 
| Gestión (1799)| 10.10.17.56/29   | 255.255.255.248  | 10.10.17.57 – 10.10.17.62 | 10.10.17.63         | 6            | 10.10.17.57        | 
| Red remota   | 10.10.17.64/30   | 255.255.255.252  | 10.10.17.65 – 10.10.17.66 | 10.10.17.67         | 2            | 10.10.17.65(R1) - 66(R2)       | 
| Rango libre  | 10.10.17.68-255  | -                | -                         | -                   | -            | -                  | 

# Configuración de Switches SW1 y SW2

## SW1 - SwitchLOCAL


**Configuración:**
```plaintext
conf t
!
hostname SwitchLOCAL
!
vlan 1799
 name VLAN_GESTION
exit
!
interface ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan 1799
exit
!
interface ethernet1/0
 switchport mode access
 switchport access vlan 1799
exit
!
do wr
```

---

## SW2 - SwitchREMOTO

**Configuración:**
```plaintext
conf t
!
hostname SwitchREMOTO
!
vlan 1799
 name VLAN_GESTION
exit
!
interface ethernet0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan 1799
exit
!
interface ethernet1/0
 switchport mode access
 switchport access vlan 1799
exit
!
do wr
```


# Configuración completa de la PC SYSADMIN en Debian 12 (PNETLab)


## 1. Verificar interfaz de red activa

Usá este comando para ver qué interfaz tenés disponible:

```bash
ip a
```

Ignorá la interfaz `lo`. La que identifiques será la que uses para configurar tu IP.

![ConfiguraciónIP](Images/IP-Debian12.png)
---

## 2. Asignar IP estática y ruta por defecto

Ejecutar los siguientes comandos (reemplazá `enp0s3` si tu interfaz tiene otro nombre):

```bash
sudo ip addr add 10.10.17.57/29 dev enp0s3
sudo ip link set enp0s3 up
sudo ip route add default via 10.10.17.59
```

- `10.10.17.57/29` → IP de tu PC SYSADMIN  
- `10.10.17.59` → IP del MikroTik que actúa como gateway

---

## 3. Verificar conectividad

Probar comunicación con la puerta de enlace, una IP pública y un dominio:

```bash
ping 10.10.17.59     # MikroTik
ping 8.8.8.8           # IP pública (Google)
ping google.com        # DNS
```

Si falla la resolución de nombres, configurar DNS:

```bash
sudo nano /etc/resolv.conf
```

Agregar:

```
nameserver 8.8.8.8
nameserver 1.1.1.1
```

---

## 4. Instalar Python y pip

Actualizar repositorios e instalar:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

Verificar versiones:

```bash
python3 --version
pip3 --version
```

---

## 5. Instalar Netmiko

Instalar el módulo para conexiones SSH en red:

```bash
pip3 install netmiko
```

> Esto también instalará Paramiko para conexiones SSH.

---

## 6. Instalar wget (opcional)

Si no está instalado, hacerlo con:

```bash
sudo apt install wget
```

---

## 7. Descargar el script desde GitHub

Usar `wget` para obtener el archivo en formato RAW:

```bash
wget https://raw.githubusercontent.com/Gordopolis9/RED-WITH-NETMIKO/master/test_netmiko_connect.py
```

**Cómo obtener el enlace RAW:**

1. Abrir el archivo en GitHub.  
2. Clic en "Raw".  
3. Copiar la URL del navegador.

---

## 8. Ejecutar el script

Ejecutar el archivo Python:

```bash
python3 test_netmiko_connect.py
```

> Este script se conecta por SSH a tus routers y switches para ejecutar comandos de prueba.

---

## Extras útiles

Ver contenido del script:

```bash
cat test_netmiko_connect.py
```

Editar el script:

```bash
nano test_netmiko_connect.py
```

---

Con esto, tu PC SYSADMIN queda lista para automatizar configuraciones de red con Python y Netmiko.
