from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Base de datos temporal en memoria
inventario = [
    {
        "id": "PROD01",
        "nombre": "Martillo de Uña 16oz",
        "cantidad": 12,
        "precio": 15.00,
        "iva": 2.85,
        "total": 17.85,
        "fecha_compra": "2026-01-10",
        "fecha_venta": "N/A",
        "agotado": False
    },
    {
        "id": "PROD02",
        "nombre": "Taladro Inalámbrico 20V",
        "cantidad": 0,
        "precio": 85.00,
        "iva": 16.15,
        "total": 101.15,
        "fecha_compra": "2026-02-01",
        "fecha_venta": "2026-03-01",
        "agotado": True
    }
]

PORCENTAJE_IVA = 0.19  # 19% de IVA configurable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    return jsonify(inventario)

@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    datos = request.json
    
    precio = float(datos.get('precio', 0))
    cantidad = int(datos.get('cantidad', 0))
    iva_calculado = round(precio * PORCENTAJE_IVA, 2)
    total_calculado = round(precio + iva_calculado, 2)
    
    nuevo_producto = {
        "id": datos.get('id'),
        "nombre": datos.get('nombre'),
        "cantidad": cantidad,
        "precio": precio,
        "iva": iva_calculado,
        "total": total_calculado,
        "fecha_compra": datos.get('fecha_compra'),
        "fecha_venta": datos.get('fecha_venta') if datos.get('fecha_venta') else "N/A",
        "agotado": cantidad <= 0
    }
    
    inventario.append(nuevo_producto)
    return jsonify({"mensaje": "Producto guardado con éxito", "producto": nuevo_producto}), 201

if __name__ == '__main__':
    app.run(debug=True)