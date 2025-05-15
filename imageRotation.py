# Librerías
from PIL import Image
import numpy as np

# Carga la imagen y conviértela a escala de grises
imagen = Image.open("imagenOriginal.JPG").convert("L")
arr = np.array(imagen)

# Recorta a un cuadrado de lado TAM
TAM = min(arr.shape)
arr = arr[:TAM, :TAM]

# Genera 3 versiones con 1, 5 y 10 iteraciones
for n in [1, 5, 10]:
    transform = arr.copy()

    # Aplica n veces el Arnold Cat Map
    for _ in range(n):
        nueva = np.zeros_like(transform)
        for y in range(TAM):              
            for x in range(TAM):        
                px = (x + y) % TAM
                py = (x + 2*y) % TAM
                nueva[py][px] = transform[y][x]
        transform = nueva

    # 4) Guarda la versión transformada
    fname = f"transform_{n}iter.jpg"
    Image.fromarray(transform).save(fname)

    # 5) Calcula % de píxeles idénticos respecto al original
    iguales = np.sum(transform == arr)
    porcent = iguales * 100.0 / transform.size
    print(f"{n} iter → {porcent:.2f}% píxeles idénticos")

# 6) Busca cuántas iteraciones hacen falta para recuperar la original
current = arr.copy()
count = 0
MAX_ITERACIONES = 5000
while True:
    count += 1
    nueva = np.zeros_like(current)
    for y in range(TAM):
        for x in range(TAM):
            px = (x + y) % TAM
            py = (x + 2*y) % TAM
            nueva[py][px] = current[y][x]
    current = nueva

    # Cuando vuelve a coincidir completamente, guardamos y rompemos
    if (current == arr).all():
        Image.fromarray(current).save("recuperada.jpg")
        print(f"Recuperada en {count} iteraciones")
        break
    if count >= MAX_ITERACIONES:
        print(f"No recuperó en {MAX_ITERACIONES} iteraciones, abortando.")
        break