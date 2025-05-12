

# Register your models here.
from django.contrib import admin
from .models import Usuario, Cafeteria, Empleado, Producto, Pedido, Cliente, Reserva

@admin.register(Cafeteria)
class CafeteriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad')
    search_fields = ('nombre', 'ciudad')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puesto', 'cafeteria')
    list_filter = ('cafeteria', 'puesto')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'producto', 'fecha', 'cantidad')
    list_filter = ('fecha',)
    search_fields = ('empleado__nombre', 'producto__nombre')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email')
    search_fields = ('nombre', 'email')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'cafeteria', 'fecha_hora', 'personas')
    list_filter = ('cafeteria', 'fecha_hora')
    search_fields = ('cliente__nombre',)

admin.site.register(Usuario)



