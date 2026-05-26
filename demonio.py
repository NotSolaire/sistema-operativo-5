import os
import time
import threading
import shutil

BASE_DIR = os.path.expanduser("~/servidor_archivos")
ENTRADA_DIR = os.path.join(BASE_DIR, "entrada")
PROCESADOS_DIR = os.path.join(BASE_DIR, "procesados")
LOG_FILE = os.path.join(BASE_DIR, "logs", "registro.log")

# El demonio comparte el mismo criterio de sincronización mediante exclusión mutua
log_lock = threading.Lock()
archivo_lock = threading.Lock()

def registrar_log_demonio(mensaje):
    with log_lock:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[DEMONIO] {mensaje}\n")
    print(f"[DEMONIO] {mensaje}")

def procesar_archivo_hilo(nombre_archivo):
    """Lógica que ejecuta el hilo secundario lanzado por el demonio."""
    ruta_origen = os.path.join(ENTRADA_DIR, nombre_archivo)
    ruta_destino = os.path.join(PROCESADOS_DIR, nombre_archivo)
    
    with archivo_lock:
        if os.path.exists(ruta_origen):
            # Simulación de un procesamiento de datos elemental
            registrar_log_demonio(f"Iniciando procesamiento de: {nombre_archivo}")
            time.sleep(2) # Simular carga de procesamiento
            
            shutil.move(ruta_origen, ruta_destino)
            registrar_log_demonio(f"Procesado y movido exitosamente: {nombre_archivo}")

def monitorear_directorio():
    registrar_log_demonio("Servicio de monitoreo iniciado (Cada 10 segundos).")
    while True:
        try:
            with archivo_lock:
                archivos = [f for f in os.listdir(ENTRADA_DIR) if os.path.isfile(os.path.join(ENTRADA_DIR, f))]
            
            for archivo in archivos:
                # Lanzar un hilo independiente por cada archivo detectado
                hilo_procesador = threading.Thread(target=procesar_archivo_hilo, args=(archivo,))
                hilo_procesador.start()
                
        except Exception as e:
            registrar_log_demonio(f"Error en el ciclo de monitoreo: {e}")
            
        time.sleep(10)

if __name__ == "__main__":
    try:
        monitorear_directorio()
    except KeyboardInterrupt:
        print("\nDemonio detenido por el usuario.")
