 # Explicación e instalación script de automatización

Este script en **Python** utiliza la librería `netmiko` para conectarse
a dispositivos de red (Cisco IOS y MikroTik RouterOS) y configurar
automáticamente **VLANs, puertos, firewalls y servicios de red**.

------------------------------------------------------------------------

## 📑 Contenidos
- [Objetivo del Script](#-objetivo-del-script)
- [Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [Cómo ejecutar el script](#️-cómo-ejecutar-el-script)
- [Estructura del Script](#-estructura-del-script)
- [Listado de Menús](#-listado-de-menús)


------------------------------------------------------------------------

## 📌 Objetivo del Script

-   Automatizar la **configuración de switches y routers** en una red
    local y remota.
-   Crear y configurar **VLANs** en dispositivos Cisco y MikroTik.
-   Configurar **puertos de acceso y troncales** en switches.
-   Asignar **direcciones IP** a las VLANs en routers.
-   Implementar **reglas de firewall** y **servicios DHCP** en MikroTik.
-   Probar conexiones SSH con todos los dispositivos.
-   Ofrecer un menú interactivo para gestionar la red.

------------------------------------------------------------------------

## ⚙️ Tecnologías Utilizadas

-   Python 3
-   Netmiko → Para conexión SSH y envío de comandos a dispositivos de
    red.
-   ipaddress → Para gestionar subredes y direcciones IP en MikroTik.
-   os → Para limpiar pantalla y gestionar la interfaz de menú.

------------------------------------------------------------------------
## ▶️ Cómo ejecutar el script

-   La PC desde donde se ejecuta debe tener conexión a Internet para
    descargar dependencias e instalar el script.
   
-   Debe poder conectarse por red a los dispositivos configurados en el
    diccionario devices.
    
-   Los dispositivos deben tener habilitado el servicio SSH.

> Para esto revise la documentación del equipo Sysadmin -> [Configuración de la PC SYSADMIN](/Docs/03_Config-SYSADMIN.md)
------------------------------------------------------------------------

## 📂 Estructura del Script

### 1. Definición de dispositivos (`devices`)

Se definen los dispositivos de red (switches y routers) con sus
parámetros de conexión:

-   `device_type`: Tipo de dispositivo (`cisco_ios` o
    `mikrotik_routeros`).
-   `host`: Dirección IP de gestión.
-   `username`, `password`: Credenciales de acceso.
-   `secret`: Clave adicional para Cisco IOS.
-   `port`: Puerto SSH para MikroTik.

### 2. Definición de VLANs (`vlans`)

Se definen las VLANs con su nombre, ID y direcciones IP asociadas.

Ejemplo:

``` python
{'VLAN_NAME' : 'VLAN_VENTAS', 'VLAN_ID' : 280, 'VLAN_GATEWAY' : "10.10.17.1/27"}
```

### 3. Funciones principales

#### 🔹 `create_SW_vlans(connection, name)`

-   Comprueba si una VLAN existe en el switch Cisco.
-   Si no existe, la crea con su nombre e ID.

#### 🔹 `sw1_local()`

-   Conecta al **Switch Local** (`SW1`).
-   Crea VLANs necesarias.
-   Configura puertos de acceso (`e0/1`, `e0/2`, `e0/3`).
-   Configura un puerto **troncal** (`e0/0`) con VLANs permitidas.

#### 🔹 `sw2_remoto()`

-   Similar a `sw1_local()`, pero aplicado al **Switch Remoto** (`SW2`).
-   Configura solo el puerto **troncal**.

#### 🔹 `r1_local()`

-   Conecta al **Router Local** (MikroTik).
-   Crea interfaces VLAN con sus direcciones IP.
-   Configura reglas de **firewall** (bloqueo para visitantes).
-   Configura servidor **DHCP** para VLAN de visitantes.

#### 🔹 `test_connections()`

-   Verifica conexión SSH con todos los dispositivos.

#### 🔹 `configure_network()`

Menú para: 1. Ver configuración preestablecida. 2. Iniciar configuración
automática de la red. 3. (Pendiente) Eliminar configuración existente.

#### 🔹 `menu_dispositivos()`

Muestra un listado de dispositivos disponibles para conectarse.

#### 🔹 `show_config()`

-   Ejecuta comandos en Cisco y MikroTik para mostrar la configuración
    actual:
    -   Cisco: `show ip interface brief`, `show vlan brief`
    -   MikroTik: `/interface print`, `/ip address print`,
        `/ip firewall filter print`, etc.

#### 🔹 `settings_menu()`

Permite modificar configuraciones desde el menú: - Cambiar parámetros de
**dispositivos** (host, usuario, contraseña, secret/port). - Cambiar
parámetros de **VLANs** (ID, direcciones IP/gateway).

#### 🔹 `main_menu()`

Menú principal del script: 1. Testear conexiones SSH. 2. Mostrar
configuraciones de red. 3. Configurar red automáticamente. 4. Ajustes
(settings). 0. Salir.

------------------------------------------------------------------------

## 📋 Listado de Menús

### Menú Principal

1.  Testear conexiones SSH → Verifica acceso a todos los dispositivos.
2.  Mostrar configuraciones → Ejecuta comandos y muestra estado actual.
3.  Configurar red (Automático) → Crea VLANs, puertos y DHCP en red.
4.  Ajustes (Settings) → Permite editar dispositivos y VLANs.
0.  Salir

### Menú Configuración Automática (configure_network)

1.  Ver configuración preestablecida.
2.  Iniciar configuración automática.
3.  Eliminar configuración existente (pendiente).
0.  Volver al menú principal.

### Menú Ajustes (settings_menu)

1.  Configurar dispositivos (IP, usuario, contraseña, secret/port).
2.  Configurar VLANs (ID, gateway o dirección).
0.  Volver.



