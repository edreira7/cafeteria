# core/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cafeteria, Empleado, Producto, Pedido, Cliente, Reserva
import json


# ====== Cafeterias ======
@csrf_exempt
def cafeteria_list_create(request):
    if request.method == 'GET':
        nombre = request.GET.get('nombre')
        ciudad = request.GET.get('ciudad')

        cafeterias = Cafeteria.objects.all()
        if nombre:
            cafeterias = cafeterias.filter(nombre__icontains=nombre)
        if ciudad:
            cafeterias = cafeterias.filter(ciudad__icontains=ciudad)

        data = list(cafeterias.values())
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        cafeteria = Cafeteria.objects.create(
            nombre=data['nombre'],
            direccion=data['direccion'],
            ciudad=data['ciudad']
        )
        return JsonResponse({"id": cafeteria.id, "nombre": cafeteria.nombre})


@csrf_exempt
def cafeteria_detail(request, id):
    try:
        cafeteria = Cafeteria.objects.get(id=id)
    except Cafeteria.DoesNotExist:
        return JsonResponse({"error": "Cafeteria no encontrada"}, status=404)

    if request.method == 'GET':
        return JsonResponse({"nombre": cafeteria.nombre, "direccion": cafeteria.direccion, "ciudad": cafeteria.ciudad})

    elif request.method in ['PUT', 'PATCH']:
        data = json.loads(request.body)
        cafeteria.nombre = data.get('nombre', cafeteria.nombre)
        cafeteria.direccion = data.get('direccion', cafeteria.direccion)
        cafeteria.ciudad = data.get('ciudad', cafeteria.ciudad)
        cafeteria.save()
        return JsonResponse({"id": cafeteria.id, "nombre": cafeteria.nombre})

    elif request.method == 'DELETE':
        cafeteria.delete()
        return JsonResponse({"message": "Cafeteria eliminada"}, status=204)


# ====== Empleados ======
@csrf_exempt
def empleado_list_create(request):
    if request.method == 'GET':
        cafeteria_id = request.GET.get('cafeteria')
        empleados = Empleado.objects.all().select_related('cafeteria')
        if cafeteria_id:
            empleados = empleados.filter(cafeteria_id=cafeteria_id)
        data = list(empleados.values('id', 'nombre', 'puesto', 'cafeteria__nombre'))
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        empleado = Empleado.objects.create(
            nombre=data['nombre'],
            puesto=data['puesto'],
            cafeteria_id=data['cafeteria_id']
        )
        return JsonResponse({"id": empleado.id, "nombre": empleado.nombre, "puesto": empleado.puesto})


@csrf_exempt
def empleado_detail(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
    except Empleado.DoesNotExist:
        return JsonResponse({"error": "Empleado no encontrado"}, status=404)

    if request.method == 'PATCH':
        data = json.loads(request.body)
        empleado.puesto = data.get('puesto', empleado.puesto)
        empleado.save()
        return JsonResponse({"id": empleado.id, "nombre": empleado.nombre, "puesto": empleado.puesto})

    elif request.method == 'DELETE':
        empleado.delete()
        return JsonResponse({"message": "Empleado eliminado"}, status=204)


# ====== Productos ======
@csrf_exempt
def producto_list_create(request):
    if request.method == 'GET':
        tipo = request.GET.get('tipo')
        productos = Producto.objects.all()
        if tipo:
            productos = productos.filter(tipo__iexact=tipo)
        data = list(productos.values('id', 'nombre', 'precio', 'tipo'))
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        producto = Producto.objects.create(
            nombre=data['nombre'],
            precio=data['precio'],
            tipo=data['tipo']
        )
        return JsonResponse(
            {"id": producto.id, "nombre": producto.nombre, "precio": producto.precio, "tipo": producto.tipo})


@csrf_exempt
def producto_detail(request, id):
    try:
        producto = Producto.objects.get(id=id)
    except Producto.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)

    if request.method in ['PUT', 'PATCH']:
        data = json.loads(request.body)
        producto.nombre = data.get('nombre', producto.nombre)
        producto.precio = data.get('precio', producto.precio)
        producto.tipo = data.get('tipo', producto.tipo)
        producto.save()
        return JsonResponse(
            {"id": producto.id, "nombre": producto.nombre, "precio": producto.precio, "tipo": producto.tipo})

    elif request.method == 'DELETE':
        producto.delete()
        return JsonResponse({"message": "Producto eliminado"}, status=204)


# ====== Pedidos ======
@csrf_exempt
def pedido_list_create(request):
    if request.method == 'GET':
        empleado_id = request.GET.get('empleado')
        producto_id = request.GET.get('producto')

        pedidos = Pedido.objects.select_related('empleado', 'producto').all()
        if empleado_id:
            pedidos = pedidos.filter(empleado_id=empleado_id)
        if producto_id:
            pedidos = pedidos.filter(producto_id=producto_id)

        data = list(pedidos.values(
            'id',
            'empleado__nombre',
            'producto__nombre',
            'fecha',
            'cantidad'
        ))
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        pedido = Pedido.objects.create(
            empleado_id=data['empleado_id'],
            producto_id=data['producto_id'],
            cantidad=data['cantidad']
        )
        return JsonResponse({
            "id": pedido.id,
            "empleado": pedido.empleado.nombre,
            "producto": pedido.producto.nombre,
            "cantidad": pedido.cantidad
        })


# ====== Clientes ======
@csrf_exempt
def cliente_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cliente = Cliente.objects.create(
            nombre=data['nombre'],
            email=data['email']
        )
        return JsonResponse({"id": cliente.id, "nombre": cliente.nombre, "email": cliente.email})


# ====== Reservas ======
@csrf_exempt
def reserva_list_create(request):
    if request.method == 'GET':
        ciudad = request.GET.get('ciudad')

        reservas = Reserva.objects.select_related('cliente', 'cafeteria').all()
        if ciudad:
            reservas = reservas.filter(cafeteria__ciudad__iexact=ciudad)

        data = list(reservas.values(
            'id',
            'cliente__nombre',
            'cafeteria__nombre',
            'fecha_hora',
            'personas'
        ))
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        reserva = Reserva.objects.create(
            cliente_id=data['cliente_id'],
            cafeteria_id=data['cafeteria_id'],
            fecha_hora=data['fecha_hora'],
            personas=data['personas']
        )
        return JsonResponse({
            "id": reserva.id,
            "cliente": reserva.cliente.nombre,
            "cafeteria": reserva.cafeteria.nombre,
            "fecha_hora": reserva.fecha_hora,
            "personas": reserva.personas
        })


@csrf_exempt
def reserva_detail(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
    except Reserva.DoesNotExist:
        return JsonResponse({"error": "Reserva no encontrada"}, status=404)

    if request.method == 'DELETE':
        reserva.delete()
        return JsonResponse({"message": "Reserva eliminada"}, status=204)


