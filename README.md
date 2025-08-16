# Proyecto de Red con VLAN Gestión y Automatización con NETMIKO

Este repositorio contiene la documentación y los scripts para el despliegue de una red con una VLAN de gestión y la configuración automática mediante Python + Netmiko.

## Requisitos previos

- Topología de red con al menos:
  - 2 Routers MikroTik
  - 2 Switches Cisco (o equivalentes en laboratorio)
  - 1 PC SYSADMIN con Debian 12
- VLAN de gestión configurada para permitir la conexión de automatización.
- Python 3.x instalado con las librerías necesarias (`netmiko`).
- Acceso a los dispositivos vía SSH.

## Contenidos

1. [Diagrama y elementos de RED](/Docs/01_Diagrama.md)
2. [Configuración VLAN Gestión](/Docs/02_VLAN-GESTION.md)
3. [Configuración de la PC SYSADMIN](/Docs/03_Config-SYSADMIN.md)
4. [Automatización con Netmiko](/Docs/04_Automatización.md)

## Scripts

Los scripts de automatización se encuentran en la carpeta [`/scripts`](../scripts).

---

## Autoría

- **Autor:** Valentín Soverón Iselle  
- **Institución:** Instituto Técnico Dr. Emilio Lamarca  
- **Fecha:** Agosto 2025  
