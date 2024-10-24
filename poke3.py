# Importación de bibliotecas necesarias
import requests        # Para hacer peticiones HTTP a la API
import json           # Para manejar datos en formato JSON
import os             # Para operaciones del sistema de archivos
from PIL import Image # Para manejar imágenes
from urllib.request import urlopen  # Para abrir URLs
import matplotlib.pyplot as plt     # Para mostrar imágenes y gráficos


def crear_carpeta_pokedex():
    """Crea la carpeta 'pokedex' si no existe."""
    if not os.path.exists('pokedex'): #Verifica la existencia de la carpeta
        os.makedirs('pokedex')        #Crea la carpeta si no existe

        print("Carpeta 'pokedex' creada exitosamente.")

def obtener_info_pokemon(pokemon_id_or_name):
    """Obtiene la información del Pokémon desde la API."""
    try:
        #crea la url de la api con el nombre o id del pokemon
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id_or_name.lower()}"
        respuesta = requests.get(url)  #hace peticion http
        respuesta.raise_for_status()  # Lanza una excepción si hay error
        return respuesta.json() #devuelve los datos de forma JSON
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener información del Pokémon: {e}")
        return None

def mostrar_imagen_pokemon(datos):
    """Muestra la imagen del Pokémon."""
    try:
        url_imagen = datos["sprites"]["front_default"]
        if url_imagen:
            imagen = Image.open(urlopen(url_imagen)) #abre la imagen desde la url
            plt.figure(figsize=(5, 5))                #crea una figura de 5x5
            plt.title(datos["name"].capitalize())    #añade el titulo
            plt.imshow(imagen)                    #muestra la imagen

            plt.axis('off')  #Oculta los ejes
            plt.show()         #muestra la figura
            return url_imagen
        else:
            print("Este Pokémon no tiene imagen disponible.")
            return None
    except Exception as e:
        print(f"Error al mostrar la imagen del Pokémon: {e}")
        return None

def mostrar_info_pokemon(datos):
    """Muestra la información del Pokémon."""
    try:
        print("\n=== INFORMACIÓN DEL POKÉMON ===")
        print(f"Nombre: {datos['name'].capitalize()}")  #muestra el nombre del pokemon

        print(f"ID: {datos['id']}")   #muestra el id del pokemon

        print(f"Tipos: {', '.join(tipo['type']['name'] for tipo in datos['types'])}")   #muestra los tipos del pokemon

        print(f"Habilidades: {', '.join(habilidad['ability']['name'] for habilidad in datos['abilities'])}")   #muestra las habilidades del pokemon

        print("\nMovimientos principales:")   #muestra los movimientos principales del pokemon

        for i, movimiento in enumerate(datos['moves'][:5], 1):   #muestra los 5 movimientos principales

            print(f"{i}. {movimiento['move']['name']}")
        print("...")
    except KeyError as e:
        print(f"Error al mostrar información: Falta el campo {e}")

def guardar_info_pokemon(datos):
    """Guarda la información del Pokémon en un archivo JSON."""
    try:
        url_imagen = datos["sprites"]["front_default"]
        #  Crea un archivo JSON con la información del Pokémon

        info_pokemon = {
            "nombre": datos["name"],
            "id": datos["id"],
            "tipos": [tipo["type"]["name"] for tipo in datos["types"]],
            "habilidades": [habilidad["ability"]["name"] for habilidad in datos["abilities"]],
            "movimientos": [movimiento["move"]["name"] for movimiento in datos["moves"][:10]],  # Limitamos a 10 movimientos
            "imagen_url": url_imagen
        }
        #crea el nombre del archivo
        filename = f'pokedex/{datos["name"]}.json'
        #guarda la información en el archivo json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(info_pokemon, f, indent=4, ensure_ascii=False)
        print(f"\nInformación guardada en: {filename}")
        
        # Verificar que el archivo se creó y contiene la URL de la imagen
        with open(filename, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
            if saved_data.get('imagen_url') != url_imagen:
                print("¡Advertencia! La URL de la imagen no se guardó correctamente.")
            else:
                print("URL de la imagen guardada correctamente.")
                
    except Exception as e:
        print(f"Error al guardar la información: {e}")

def buscar_pokemon():
    """Busca un Pokémon por ID o nombre."""
    #solicita un input al usuario con id o nombre del pokemon, o salir del programa 
    pokemon_id_or_name = input("\nIngresa el ID o nombre del Pokémon (o 'salir' para terminar): ").strip()
    
    if pokemon_id_or_name.lower() == 'salir':
        return False   #Termina el programa si el usuario escribe "salir"
    
    if not pokemon_id_or_name:
        print("Por favor, ingresa un ID o nombre válido.")
        return True     #continúa buscando si el usuario no ingresa nada

    #obtiene y muestra la  información del pokemon

    datos = obtener_info_pokemon(pokemon_id_or_name)
    if datos:
        mostrar_imagen_pokemon(datos)
        mostrar_info_pokemon(datos)
        guardar_info_pokemon(datos)
    return True #continua el programa 

def main():
    print("=== POKEDEX ===")
    crear_carpeta_pokedex()  #crea la carpeta pokedex si no existe

    while True:               #bucle principal del programa 
        if not buscar_pokemon():
            print("\nSaliendo del programa...")
            break
#verifica si el scrip se esta ejecutando directamente 
if __name__ == "__main__":
    main()