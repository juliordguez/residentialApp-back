import os
from mysql import connector
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def test():
    # Configuración desde .env
    config_map = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT')),
        'database': os.getenv('DB_NAME'),
    }

    try:
        # Conexión a la base de datos
        conn = connector.connect(**config_map)
        with conn:
            with conn.cursor() as cur:
                # Consulta a la base de datos
                sentence = 'SELECT * FROM roles'
                cur.execute(sentence)
                res = cur.fetchall()
                print(res)  # Imprimir resultados
    except Exception as err:
        print(f"Error: {err}")

# Llamar la función
if __name__ == "__main__":
    test()
