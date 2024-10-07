import requests
from owslib.wms import WebMapService
import matplotlib.pyplot as plt
from skimage import io
import cartopy.crs as ccrs
import numpy as np

latitude = float(open("latitude.txt", "r").read().strip())
longitude = float(open("longitude.txt", "r").read().strip())

# Conectar ao serviço WMS do GIBS para Landsat
wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi', version='1.1.1')

# Solicitar a imagem Landsat com base nos parâmetros (incluindo data e localização)
img = wms.getmap(layers=['Landsat_WELD_CorrectedReflectance_Bands157_Global_Annual'],
                 bbox=(longitude - 0.05, latitude - 0.05, longitude + 0.05, latitude + 0.05),  # Substituir pelas coordenadas de latitude e longitude
                 size=(800, 800),  # Tamanho da imagem
                 srs='EPSG:4326',  # Sistema de referência espacial correto
                 time='2022-05-01',  # Data fornecida pelo usuário
                 format='image/png',  # Formato da imagem
                 transparent=True)

# Salvar a imagem em um arquivo
with open('landsat_image.png', 'wb') as out_file:
    out_file.write(img.read())

# Exibir a imagem
image = io.imread('landsat_image.png')
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
ax.imshow(image, extent=(longitude - 0.05, longitude + 0.05, latitude - 0.05, latitude + 0.05), origin='upper')
plt.show()

# Calcular a cor média, ignorando o canal alfa
mean_color_rgb = np.mean(image[:, :, :3], axis=(0, 1))

# Converter a cor média para hexadecimal
mean_color_hex = "#{:02x}{:02x}{:02x}".format(int(mean_color_rgb[0]), int(mean_color_rgb[1]), int(mean_color_rgb[2]))

print(f"Cor média da imagem (RGB): {mean_color_rgb}")
print(f"Cor média da imagem (Hex): {mean_color_hex}")
