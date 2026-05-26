Benjamin Molina Delgado

# Sistema Multipropósito: Terminal, Hilos y Sincronización

Este proyecto consiste en un Sistema Cliente-Servidor de Gestión de Archivos Remotos desarrollado en Python. La aplicación integra conceptos de administración de entornos Linux, redes mediante Sockets TCP, programación concurrente con Multithreading y mecanismos de sincronización para evitar condiciones de carrera.

La arquitectura permite a múltiples clientes interactuar de forma simultánea con el servidor mientras un proceso Demonio (Worker) automatiza el procesamiento de datos en segundo plano.

---

## Qué hace el código

El sistema se divide en tres componentes principales que trabajan en conjunto:

1. **Servidor (`servidor.py`):** * Se ejecuta de forma continua escuchando conexiones entrantes en un puerto específico.
   * Por cada cliente que se conecta, el servidor levanta un hilo (Thread) independiente para atenderlo. Esto permite que múltiples usuarios listen, suban o descarguen archivos al mismo tiempo sin que el sistema se bloquee.
   * Utiliza candados (Locks) de exclusión mutua para asegurar que ningún hilo corrompa el archivo de registro o manipule un archivo que está siendo modificado por otro componente.

2. **Cliente (`cliente.py`):**
   * Proporciona una interfaz de menú interactiva en la terminal para el usuario.
   * Permite listar los archivos disponibles en el servidor, subir archivos locales al directorio remoto, descargar archivos del servidor a la máquina local y consultar el historial de operaciones (logs) en tiempo real.

3. **Demonio (`demonio.py`):**
   * Es un proceso que corre de forma autónoma y en segundo plano.
   * Monitorea la carpeta de entrada cada 10 segundos. Si detecta que un cliente subió un archivo nuevo, genera un hilo secundario para procesarlo de forma aislada.
   * Una vez procesado el archivo, lo mueve físicamente a la carpeta de procesados para mantener limpio el buzón de entrada.

---

## Estructura de Directorios

El sistema opera sobre una estructura específica ubicada en el directorio Home del usuario:

* `~/servidor_archivos/entrada/`: Carpeta donde se depositan los archivos iniciales y las subidas de los clientes.
* `~/servidor_archivos/procesados/`: Carpeta destino donde el Demonio almacena los archivos procesados.
* `~/servidor_archivos/logs/`: Carpeta que contiene el archivo compartido `registro.log`.

---

## Instrucciones de Configuración y Ejecución

Siga estos pasos estrictamente en su terminal de Linux para replicar el entorno y demostrar la concurrencia del sistema.

### Paso 1: Preparación del Entorno y Permisos

Ejecute los siguientes comandos en la terminal para inicializar las carpetas y restringir los accesos directos:


# Crear la estructura de carpetas requerida
mkdir -p ~/servidor_archivos/entrada ~/servidor_archivos/procesados ~/servidor_archivos/logs

# Asignar permisos restrictivos (lectura, escritura y ejecución solo para el dueño)
chmod -R 700 ~/servidor_archivos

# Crear archivos de prueba con datos aleatorios en el directorio de entrada
echo "Datos aleatorios del archivo 1" > ~/servidor_archivos/entrada/archivo1.txt
echo "Datos aleatorios del archivo 2" > ~/servidor_archivos/entrada/archivo2.txt
echo "Datos aleatorios del archivo 3" > ~/servidor_archivos/entrada/archivo3.txt
# ver la ip del servidor
abrir el cmd  escribir ipconfing y buscar los datos en 
Adaptador de LAN inalámbrica Wi-Fi 2:
   Dirección IPv4. . . . . . . . . . . . . . IP: 12.345.67.8 
