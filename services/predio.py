from flask import Blueprint, request, jsonify
from model.predio import Predio
from utils.db import db
from flask import render_template,redirect, url_for
import json
import requests

predios =Blueprint('predios',__name__)

@predios.route('/predios/v1',methods=['GET'])
def getMensaje():
    result={}
    result["data"]='flask-crud-backend'
    return jsonify(result)

@predios.route('/predios/v1/obtener-datos', methods=['POST',"GET"])
def obtener_datos():
    if request.method == 'GET':
        return render_template('dni.html', datos=None)
    
    dato_input = request.form['dato_input']
    # Aquí puedes hacer lo que quieras con los datos obtenidos, como imprimirlos o procesarlos de alguna manera.
    #Definir el número de DNI y el token de autorización
    dni = dato_input 
    token = "bae023f136b094b6dfa7872343f370e2e9e7036ff927dfdbeaa483202c5f1fe6"

    # URL de la API
    url = "https://apiperu.dev/api/dni"

    # Construir el payload como un diccionario
    payload = {
        "dni": dni
    }

    # Convertir el payload a formato JSON
    params = json.dumps(payload)

    # Configurar los encabezados de la solicitud
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Realizar la solicitud POST
    response = requests.post(url, data=params, headers=headers)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # La solicitud fue exitosa
        data = response.json()
        dataPass = data["data"]
        return render_template('dni.html', datos=dataPass)
    else:
        # Hubo un error en la solicitud
        return render_template('dni.html', datos=None)


@predios.route('/predios/v1/listartabla', methods=['GET'])
def listartabla():
    predios = Predio.query.all()  
    return render_template('data.html', predios=predios)


@predios.route('/predios/v1/listar',methods=['GET'])
def getContactos():
    result={}
    predios = Predio.query.all()    
    result["data"]=predios
    result["status_code"]=200
    result["msg"]="Se recupero los predios sin inconvenientes"
    return jsonify(result),200

@predios.route('/predios/v1/insert',methods=['POST'])
def insert():
    result = {}
    body = request.get_json()
    
    id_tipo_predio = body.get('id_tipo_predio')
    descripcion = body.get('descripcion')
    ruc = body.get('ruc')
    telefono = body.get('telefono')
    correo = body.get('correo')
    direccion = body.get('direccion')
    idubigeo = body.get('idubigeo')
    id_persona = body.get('id_persona')
    url_imagen = body.get('url_imagen')

    if  not id_tipo_predio or not descripcion or not ruc or not telefono or not correo or not direccion or not idubigeo or not id_persona or not url_imagen:
        result["status_code"] = 400
        result["msg"] = "faltan datos"
        return jsonify(result),400
   
    predio = Predio(
    id_tipo_predio=id_tipo_predio,
    descripcion=descripcion,
    ruc=ruc,
    telefono=telefono,
    correo=correo,
    direccion=direccion,
    idubigeo=idubigeo,
    id_persona=id_persona,
    url_imagen=url_imagen)

    db.session.add(predio)
    db.session.commit()
    result["data"]= predio
    result["status_code"]=201
    result["msg"] = "inserto correctamente"
    return jsonify(result),201


@predios.route('/predios/v1/update',methods=['POST'])
def update():
    result = {}
    
    body = request.get_json()

    id_predio = body.get('id_predio')
    id_tipo_predio = body.get('id_tipo_predio')
    descripcion = body.get('descripcion')
    ruc = body.get('ruc')
    telefono = body.get('telefono')
    correo = body.get('correo')
    direccion = body.get('direccion')
    idubigeo = body.get('idubigeo')
    id_persona = body.get('id_persona')
    url_imagen = body.get('url_imagen')

    if  not id_predio or not id_tipo_predio or not descripcion or not ruc or not telefono or not correo or not direccion or not idubigeo or not id_persona or not url_imagen:
        result["status_code"] = 400
        result["msg"] = "faltan datos"
        return jsonify(result),400
    
    predio = Predio.query.get(id_predio)

    predio.id_predio = id_predio
    predio.id_tipo_predio = id_tipo_predio
    predio.descripcion = descripcion
    predio.ruc = ruc
    predio.telefono = telefono
    predio.correo = correo
    predio.direccion = direccion
    predio.idubigeo = idubigeo
    predio.id_persona = id_persona
    predio.url_imagen = url_imagen

    db.session.add(predio)
    db.session.commit()

    result["data"]= predio
    result["status_code"]=202
    result["msg"] = "Se modifico el predio..."
    return jsonify(result),202

@predios.route('/predios/v1/delete',methods=['DELETE'])
def delete():
    result={}
    body=request.get_json()
    id_predio=body.get("id_predio")
    if not id_predio:
        result["status_code"]=400
        result["msg"]="Debe consignar un id valido"
        return jsonify(result), 400
    
    predio = Predio.query.get(id_predio)
    if not predio:
        result["status_code"]=400
        result["msg"]="Predio no encontrado"
        return jsonify(result), 400
    
    db.session.delete(predio)
    db.session.commit()

    result["data"] = predio
    result["status_code"] = 200
    result["msg"]="Se elimino el contacto"
    return jsonify(result), 200