class CarritoDeCompras:
    def __init__(self):
        self.total = 0

    # Método público expuesto a otros objetos
    def agregar_producto(self, producto, cantidad):
        precio_subtotal = producto.obtener_precio() * cantidad
        self.total += precio_subtotal
        return self.total

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def obtener_precio(self):
        return self.precio

# --- Comunicación entre objetos ---
lapiz = Producto("Lápiz", 1.50)
mi_carrito = CarritoDeCompras()

# El objeto 'mi_carrito' envía un mensaje a 'lapiz' pidiendo su precio
mi_carrito.agregar_producto(lapiz, 3)
