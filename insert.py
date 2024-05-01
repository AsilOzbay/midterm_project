import mysql.connector


def read_image_data(file_path):
    with open(file_path, "rb") as file:
        return file.read()

def insert_data_into_database(connection, id, name, price, category, next_day_delivery, city, image_data):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO hepsiburada (id, isim, fiyat, kategori, yarınkapımda, sehir, resim) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (id, name, price, category, next_day_delivery, city, image_data))
    connection.commit()
    cursor.close()

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="newuser",
        password="12345",
        database="products",
        auth_plugin='mysql_native_password'
    )


def main():
    file_path = "C:/Users/mehme/Downloads/1.jpg"
    image_data = read_image_data(file_path)

    myDB = connect_to_database()
    insert_data_into_database(myDB, 10, "Dunspin DS-F210", 600, "ELEKTRONİK", 1, "İzmir", image_data)
    myDB.close()

if __name__ == "__main__":
    main()
