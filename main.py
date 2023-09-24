import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

ventana = None
ruta = None

def ajustarTamañoVentana(anchoImagen, altoImagen):
    global ventana
    # Asegurar que el tamaño mínimo de la ventana sea 800x600
    anchoMinimo = max(800, anchoImagen + 100)
    altoMinimo = max(600, altoImagen + 100)
    
    ventana.geometry(f"{anchoMinimo}x{altoMinimo}")

# Definimos una función que recibe el nombre de una imagen y devuelve las coordenadas de los puntos extremos del área que no es blanca
def obtenerExtremos(imagen: str) -> tuple:
    # Abrimos la imagen que nos pasan como argumento
    imagen = Image.open(imagen)
    
    # Inicializamos las variables que almacenarán los valores mínimos y máximos de X e Y
    minX = minY = float("inf")
    maxX = maxY = float("-inf")

    # Obtenemos las dimensiones de la imagen (ancho y alto)
    ancho, alto = imagen.size
    
    # Recorremos todos los píxeles de la imagen
    for y in range(alto):
        for x in range(ancho):
            pixel = imagen.getpixel((x,y))
            # Si el pixel es blanco, lo ignoramos
            if (pixel == (255,255,255)): continue
            # Si el pixel no es blanco, actualizamos los valores mínimos y máximos de x e y
            minX = min(minX, x)
            maxX = max(maxX, x)
            minY = min(minY, y)
            maxY = max(maxY, y)
    
    # Devolvemos una tupla con las coordenadas de los puntos extremos
    return (minX, minY, maxX, maxY)

# Definimos una función que recibe una imagen y las coordenadas de los puntos extremos del área que no es blanca y la mueve al borde inferior izquierdo de la imagen
def moverImagen(imagen: str, puntos: tuple) -> None:
    global ventana
    # Abrimos la imagen que nos pasan como argumento
    imagen = Image.open(imagen)
    ancho, alto = imagen.size

    # Cortamos la imagen según los puntos que nos pasan como argumento
    imagenCortada = imagen.crop((puntos[0],puntos[1],puntos[2],puntos[3]))
    
    # Creamos una nueva imagen en blanco del mismo tamaño que la original
    nuevaImagen = Image.new("RGB", (ancho,alto), (255,255,255))
    
    # Pegamos la imagen cortada en el borde inferior izquierdo de la nueva imagen
    auxX = 0
    auxY = alto - imagenCortada.height
    nuevaImagen.paste(imagenCortada, (auxX,auxY))
    nuevaImagen.save("nuevaImagen.png")

    ventana.geometry(f"{ancho}x{alto}")
    
    # Convertimos la imagen a formato PhotoImage para poder mostrarla en un widget de tkinter
    foto = ImageTk.PhotoImage(nuevaImagen)

    # Creamos un widget de tipo Label para mostrar la foto en la ventana
    etiqueta = tk.Label(ventana, image=foto)
    etiqueta.image = foto
    etiqueta.pack()
    
    # Ajustar el tamaño de la ventana
    ajustarTamañoVentana(imagenCortada.width(), imagenCortada.height())



def abrirExplorador():
    global ruta
    # Abrir el explorador de archivos y obtener la ruta de la imagen seleccionada
    rutaImagen = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
    
    if rutaImagen:
        ruta = rutaImagen
        # Obtenemos los puntos extremos del área que no es blanca de la imagen seleccionada
        puntos = obtenerExtremos(ruta)
        
        # Movemos la imagen según los puntos obtenidos
        moverImagen(ruta, puntos)
    else:
        ruta = -1
    

if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("MESSI")
    ventana.minsize(800,600)
    ventana.resizable(True, True)
    # Botón para abrir el explorador de archivos
    botonAbrir = tk.Button(ventana, text="Abrir Imagen", command=abrirExplorador)
    botonAbrir.pack()
    
    # Iniciamos el bucle principal de la ventana
    ventana.mainloop()
    
    if ruta is None:
        print("No se seleccionó ninguna imagen")
    elif ruta == -1:
        print("Ruta no válida")
