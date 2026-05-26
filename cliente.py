import socket
import os

def mostrar_menu():
    print("\n--- MENÚ GESTIÓN DE ARCHIVOS REMOTOS ---")
    print("1. Listar archivos remotos (entrada)")
    print("2. Descargar archivo del servidor")
    print("3. Subir archivo local al servidor")
    print("4. Ver logs del sistema")
    print("5. Salir")
    return input("Seleccione una opción: ")

def ejecutar_cliente(host='127.0.0.1', port=5000):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. ¿Está activo?")
        return

    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            client.send("LISTAR".encode('utf-8'))
            respuesta = client.recv(1024).decode('utf-8')
            print(f"\n[SERVIDOR] Archivos disponibles: {respuesta.replace(',', ', ')}")

        elif opcion == "2":
            nombre = input("Nombre del archivo a descargar: ")
            client.send(f"DESCARGAR {nombre}".encode('utf-8'))
            respuesta = client.recv(1024).decode('utf-8')
            if respuesta.startswith("OK"):
                contenido = respuesta[3:]
                with open(f"descargado_{nombre}", "w", encoding="utf-8") as f:
                    f.write(contenido)
                print(f"[ÉXITO] Archivo guardado localmente como 'descargado_{nombre}'")
            else:
                print("[ERROR] El archivo no existe en el servidor.")

        elif opcion == "3":
            ruta_local = input("Ingrese la ruta del archivo local a subir: ")
            if os.path.exists(ruta_local):
                nombre = os.path.basename(ruta_local)
                client.send(f"SUBIR {nombre}".encode('utf-8'))
                
                # Esperar confirmación de listo
                if client.recv(1024).decode('utf-8') == "READY":
                    with open(ruta_local, "r", encoding="utf-8") as f:
                        contenido = f.read()
                    client.send(contenido.encode('utf-8'))
                    
                    if client.recv(1024).decode('utf-8') == "OK":
                        print("[ÉXITO] Archivo subido correctamente.")
            else:
                print("[ERROR] El archivo local no existe.")

        elif opcion == "4":
            client.send("VER_LOGS".encode('utf-8'))
            respuesta = client.recv(4096).decode('utf-8')
            if respuesta.startswith("OK"):
                print(f"\n--- LOGS DEL SERVIDOR ---\n{respuesta[3:]}")
            else:
                print(f"[SERVIDOR] {respuesta}")

        elif opcion == "5":
            print("Desconectando...")
            break
        else:
            print("Opción inválida.")
            
    client.close()

if __name__ == "__main__":
    ejecutar_cliente()
