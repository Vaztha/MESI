import tkinter as tk
from PIL import Image, ImageTk

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
    
    # Creamos una ventana de tkinter para mostrar la imagen modificada
    ventana = tk.Tk()
    ventana.title("Imagen con cuadrado negro")
    ventana.geometry(f"{ancho}x{alto}")

    # Convertimos la imagen a formato PhotoImage para poder mostrarla en un widget de tkinter
    foto = ImageTk.PhotoImage(nuevaImagen)

    # Creamos un widget de tipo Label para mostrar la foto en la ventana
    etiqueta = tk.Label(ventana, image=foto)
    etiqueta.pack()

    # Iniciamos el bucle principal de la ventana
    ventana.mainloop()
    

if __name__ == "__main__":
    # Obtenemos los puntos extremos del área que no es blanca de la imagen "imagen.png"
    puntos = obtenerExtremos("imagen.png")
    
    # Movemos la imagen según los puntos obtenidos
    moverImagen("imagen.png", puntos)
