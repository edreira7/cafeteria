


from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo Usuario personalizado
class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='empleado')

    def __str__(self):
        return f"{self.username} ({self.rol})"

class Cafeteria(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.puesto})"

class Producto(models.Model):
    TIPOS = [
        ('cafe', 'Café'),
        ('te', 'Té'),
        ('postre', 'Postre'),
        ('otro', 'Otro')
    ]
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='otro')

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class Pedido(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} por {self.empleado.nombre}"

# Tabla adicional 1: Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

# Tabla adicional 2: Reserva
class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    personas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cliente.nombre} - {self.cafeteria.nombre} ({self.fecha_hora})"

