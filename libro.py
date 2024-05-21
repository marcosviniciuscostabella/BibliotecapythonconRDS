import mysql.connector

class Libro:
    def __init__(self, titulo, autor, precio):
        self.titulo = titulo
        self.autor = autor
        self.precio = precio

class Inventario:
    def __init__(self):
        self.libros = []
        self.conexion = mysql.connector.connect(
            host="database-1.cde6cw86e7i8.us-east-1.rds.amazonaws.com",
            user="admin",
            password="Marcos2024",
            database="libro_database_name"
        )
        self.cursor = self.conexion.cursor()
    
    def agregar_libro(self, libro):
        self.libros.append(libro)
        print("Libro agregado al inventario.")
        sql = "INSERT INTO table_name (nombre_libro, autor, precio) VALUES (%s, %s, %s)"
        valores = (libro.titulo, libro.autor, libro.precio)
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        print("Libro agregado a la base de datos.")

    def buscar_libro(self, titulo):
        encontrado = False
        for libro in self.libros:
            if libro.titulo == titulo:
                print("Información del libro:")
                print("Título:", libro.titulo)
                print("Autor:", libro.autor)
                print("Precio:", libro.precio)
                encontrado = True
                break
        if not encontrado:
            print("El libro no está en el inventario.")
        
        sql = "SELECT * FROM table_name WHERE nombre_libro = %s"
        self.cursor.execute(sql, (titulo,))
        resultado = self.cursor.fetchone()
        if resultado:
            print("Información del libro en la base de datos:")
            print("Título:", resultado[1])
            print("Autor:", resultado[2])
            print("Precio:", resultado[3])
        else:
            print("El libro no está en la base de datos.")

    def registrar_venta(self, titulo):
        for libro in self.libros:
            if libro.titulo == titulo:
                self.libros.remove(libro)
                print("Venta registrada. Libro vendido:", libro.titulo)
                break
        else:
            print("El libro no está en el inventario.")
        
        sql = "DELETE FROM table_name WHERE nombre_libro = %s"
        self.cursor.execute(sql, (titulo,))
        self.conexion.commit()
        print("Venta registrada en la base de datos.")

    def cerrar_conexion(self):
        self.cursor.close()
        self.conexion.close()

def main():
    inventario = Inventario()
    
    while True:
        print("\nMenú:")
        print("1. Agregar un nuevo libro al inventario.")
        print("2. Buscar un libro por título.")
        print("3. Registrar una venta de un libro.")
        print("4. Salir.")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            titulo = input("Ingrese el título del libro: ")
            autor = input("Ingrese el autor del libro: ")
            precio = float(input("Ingrese el precio del libro: "))
            nuevo_libro = Libro(titulo, autor, precio)
            inventario.agregar_libro(nuevo_libro)
        elif opcion == "2":
            titulo = input("Ingrese el título del libro a buscar: ")
            inventario.buscar_libro(titulo)
        elif opcion == "3":
            titulo = input("Ingrese el título del libro vendido: ")
            inventario.registrar_venta(titulo)
        elif opcion == "4":
            print("Saliendo del programa...")
            inventario.cerrar_conexion()
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()