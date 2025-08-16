# Configuración de la VLAN-GESTION

Este documento describe la **configuración de la VLAN de gestión (ID 1799)**, que permite la administración remota de los dispositivos de red de forma segura y centralizada.  
Se detallan las asignaciones de IP por dispositivo, las configuraciones aplicadas en los routers (R1 y R2) y en los switches (SW1 y SW2), así como el host SYSADMIN que forma parte de esta red de gestión.  

## Tabla de configuraciónes

| VLAN ID | Nombre           | Dispositivo | Interfaz   | Dirección IP       | Tipo     |
|---------|-----------------|-------------|------------|--------------------|----------|
| 1799    | VLAN_GESTION     | SW1 (LOCAL)         | Fa0/1      | N/A                | Access   |
| 1799    | VLAN_GESTION     | SW1 (LOCAL)         | Fa0/0      | Trunk              | Trunk    |
| 1799    | VLAN_GESTION     | SW2 (REMOTO)        | Fa0/0      | Trunk              | Trunk    |
| 1799    | VLAN_GESTION     | R1 (LOCAL)  | ether2     | 10.10.17.59/29     | Routed   |
| 1799    | VLAN_GESTION-P2P | R1 (LOCAL)  | ether3     | 10.10.17.65/30     | Routed   |
| 1799    | VLAN_GESTION-P2P | R2 (REMOTO) | ether2     | 10.10.17.66/30     | Routed   |
| 1799    | VLAN_GESTION     | SYSADMIN    | ens18      | 10.10.17.58/29  | Host     |

## Configuración de Routers R1 y R2

### R1 - RouterLOCAL

```shell
# Crear VLAN Gestión en ether2
/interface vlan
add name=VLAN_GESTION vlan-id=1799 interface=ether2

# Crear VLAN Gestión-P2P en ether3
/interface vlan
add name=VLAN_GESTION-P2P vlan-id=1799 interface=ether3

# Direcciones IP
/ip address
add address=10.10.17.59/29 interface=VLAN_GESTION
add address=10.10.17.65/30 interface=VLAN_GESTION-P2P

# Bridges
/interface bridge
add name=BRIDGE_GESTION vlan-filtering=yes

/interface bridge port
add bridge=BRIDGE_GESTION interface=VLAN_GESTION
add bridge=BRIDGE_GESTION interface=VLAN_GESTION-P2P

# Configuración de NAT para salida a Internet
/ip firewall nat
add chain=srcnat out-interface=ether1 action=masquerade
```

---

### R2 - RouterREMOTO

```shell
# Crear VLAN Gestión en ether2
/interface vlan
add name=VLAN_GESTION vlan-id=1799 interface=ether2

# Crear VLAN Gestión-P2P en ether3
/interface vlan
add name=VLAN_GESTION-P2P vlan-id=1799 interface=ether3

# Direcciones IP
/ip address
add address=10.10.17.66/30 interface=VLAN_GESTION-P2P

# Bridges
/interface bridge
add name=BRIDGE_GESTION vlan-filtering=yes

/interface bridge port
add bridge=BRIDGE_GESTION interface=VLAN_GESTION
add bridge=BRIDGE_GESTION interface=VLAN_GESTION-P2P
```


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
interface vlan 1799
 ip address 10.10.17.58 255.255.255.248
 no shutdown
exit
!
ip default-gateway 10.10.17.60
!
username admin privilege 15 secret Admin123
!
line vty 0 4
 transport input ssh
 login local
exit
!
ip domain-name redes.local
!
crypto key generate rsa modulus 1024
ip ssh version 2
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
interface vlan 1799
 ip address 10.10.17.61 255.255.255.248
 no shutdown
exit
!
ip default-gateway 10.10.17.60
!
username admin privilege 15 secret Admin123
!
line vty 0 4
 transport input ssh
 login local
exit
!
ip domain-name redes.local
!
crypto key generate rsa modulus 1024
ip ssh version 2
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