import requests

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BASE_URL = 'https://api.mercadolibre.com/'

#IMPLEMENTACION DE ENDPOINTS DE API, CONSUMIENDO OTRA API (MERCADOLIBRE)
@app.route('/countries', methods=['GET'])
def get_countries():
    response = requests.get(BASE_URL + 'sites')
    return jsonify({"Paises":response.json()})


@app.route('/categories/<id_pais>', methods=['GET'])
def get_categories(id_pais):
    response = requests.get(BASE_URL + f'sites/{id_pais}/categories')
    if response.status_code != 200:
        return jsonify ({
            "status_code":response.status_code,
            "message":"No se encontraron categorias, seguramente escribio mal el pais"
        })
    return jsonify({
        "Categorias":response.json()
    })

#IMPLEMENTACION DE API ENVIANDO DATOS PROPIOS
PROVINCIAS = [
    {
      "nombre_completo": "Provincia de Misiones",
      "fuente": "IGN",
      "iso_id": "AR-N",
      "nombre": "Misiones",
      "id": "54",
      "categoria": "Provincia",
      "iso_nombre": "Misiones",
      "centroide": {
        "lat": -26.8753965086829,
        "lon": -54.6516966230371
      }
    },
    {
      "nombre_completo": "Provincia de San Luis",
      "fuente": "IGN",
      "iso_id": "AR-D",
      "nombre": "San Luis",
      "id": "74",
      "categoria": "Provincia",
      "iso_nombre": "San Luis",
      "centroide": {
        "lat": -33.7577257449137,
        "lon": -66.0281298195836
      }
    },
    {
      "nombre_completo": "Provincia de San Juan",
      "fuente": "IGN",
      "iso_id": "AR-J",
      "nombre": "San Juan",
      "id": "70",
      "categoria": "Provincia",
      "iso_nombre": "San Juan",
      "centroide": {
        "lat": -30.8653679979618,
        "lon": -68.8894908486844
      }
    }]

@app.route('/provincias_argentinas')
def get_provincias_argentinas():
    provincias = PROVINCIAS
    return jsonify({"provincias": provincias})

#IMPLEMENTACION DE API, CONSUMIENDO Y ENVIANDO AL "FRONT"
@app.route('/', methods=['GET'])
def get_countries_for_template():
    response = requests.get(BASE_URL + 'sites')
    paises = response.json()
    return render_template(
        'index.html',
        paises=paises,
    )

# DEVOLVER CATEGORIES AL HTML

if __name__ == '__main':
    app.run(host="0.0.0.0")