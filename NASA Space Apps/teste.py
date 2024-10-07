import octas_nuvens

# Ler latitude e longitude dos arquivos
latitude = open("latitude.txt", "r").read().strip()
longitude = open("longitude.txt", "r").read().strip()

def test_library():
    try:
        # Chamar a função verificar_nuvens e verificar o resultado
        if octas_nuvens.verificar_nuvens(latitude, longitude):
            print("Biblioteca retornou True, mais de 15% de nuvens no céu.")
        else:
            print("Biblioteca retornou False, menos de 15% de nuvens no céu.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_library()
