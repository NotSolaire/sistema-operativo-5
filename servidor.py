import socket
import threading
import os
import shutil

# Configuración de rutas básicas
BASE_DIR = os.path.expanduser("~/servidor_archivos")
ENTRADA_DIR = os.path.join(BASE_DIR, "entrada")
PROCESADOS_DIR = os.path.join(BASE_DIR, "procesados")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(BASE_DIR, "logs", "registro.log")

os.makedirs(ENTRADA_DIR, exist_ok=True)
os.makedirs(PROCESADOS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Locks para evitar condiciones de carrera
log_lock = threading.Lock()
archivo_lock = threading.Lock()  # Protege la manipulación física de archivos compartidos

def registrar_log(mensaje):
    """Registra de manera sincronizada las operaciones en el archivo log."""
    with log_lock:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{mensaje}\n")
    print(mensaje)

def manejar_cliente(conn, addr):
    registrar_log(f"[CONEXIÓN] Cliente conectado desde {addr}")
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            
            comando = data.split()
            opcion = comando[0]

            if opcion == "LISTAR":
                archivos = os.listdir(ENTRADA_DIR)
                respuesta = ",".join(archivos) if archivos else "VACIO"
                conn.send(respuesta.encode('utf-8'))

            elif opcion == "LEER":
                nombre_archivo = comando[1]
                ruta = os.path.join(ENTRADA_DIR, nombre_archivo)
                with archivo_lock:
                    if os.path.exists(ruta):
                        with open(ruta, "r", encoding="utf-8") as f:
                            contenido = f.read()
                        conn.send(f"OK {contenido}".encode('utf-8'))
                    else:
                        conn.send("ERROR Archivo no encontrado".encode('utf-8'))

            elif opcion == "SUBIR":
                nombre_archivo = comando[1]
                conn.send("READY".encode('utf-8'))
                contenido = conn.recv(4096).decode('utf-8')
                
                ruta = os.path.join(ENTRADA_DIR, nombre_archivo)
                with archivo_lock:
                    with open(ruta, "w", encoding="utf-8") as f:
                        f.write(contenido)
                
                registrar_log(f"[SUBIDA] Cliente {addr} subió {nombre_archivo}")
                conn.send("OK".encode('utf-8'))

            elif opcion == "DESCARGAR":
                nombre_archivo = comando[1]
                ruta = os.path.join(ENTRADA_DIR, nombre_archivo)
                
                with archivo_lock:
                    if os.path.exists(ruta):
                        with open(ruta, "r", encoding="utf-8") as f:
                            contenido = f.read()
                        conn.send(f"OK {contenido}".encode('utf-8'))
                        registrar_log(f"[DESCARGA] Cliente {addr} descargó {nombre_archivo}")
                    else:
                        conn.send("ERROR".encode('utf-8'))

            elif opcion == "VER_LOGS":
                with log_lock:
                    if os.path.exists(LOG_FILE):
                        with open(LOG_FILE, "r", encoding="utf-8") as f:
                            contenido = f.read()
                        conn.send(f"OK {contenido}".encode('utf-8'))
                    else:
                        conn.send("ERROR No hay logs aún".encode('utf-8'))
    except Exception as e:
        registrar_log(f"[ERROR] Con el cliente {addr}: {e}")
    finally:
        conn.close()
        registrar_log(f"[DESCONEXIÓN] Cliente {addr} desconectado")

def iniciar_servidor(host='127.0.0.1', port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    registrar_log(f"[INICIO] Servidor escuchando en {host}:{port}")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        registrar_log("[APAGADO] Cerrando servidor.")
    finally:
        server.close()

if __name__ == "__main__":
    iniciar_servidor()
