from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import ForeignKey
from marshmallow import fields

from alexis import TipoDni


# creamos la aplicacion
app = Flask(__name__)



#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:contrasenia@host/nombreDB'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://BD2021:BD2021itec@143.198.156.171/sql_cometto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/modelado'



db = SQLAlchemy(app)

# Creamos una instancia Miigrate que recibe la app y db
migrate = Migrate(app, db)

ma = Marshmallow(app)




#MODELADO DE LA BASE

class Pais(db.Model):
    __tablename__ = 'pais'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)


class Provincia(db.Model):
    __tablename__ = 'provincia'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    idPais = db.Column(db.Integer, ForeignKey("pais.id"))

    pais = db.relationship("Pais")
    

class Localidad(db.Model):
    __tablename__ = 'localidad'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    idProvincia = db.Column(db.Integer, ForeignKey("provincia.id"))
    provincia = db.relationship("Provincia")


class Sexo(db.Model):
    __tablename__ = 'sexo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)


class Tipodni(db.Model):
    __tablename__ = 'tipodni'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)


class Tipousuario(db.Model):
    __tablename__ = 'tipousuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(50), nullable=False)


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contrasenia = db.Column(db.String(50), nullable=False)
    idTipousuario = db.Column(db.Integer, ForeignKey("tipousuario.id"))
    fechaCarga = db.Column(db.String(50), nullable=False)
    idPersona = db.Column(db.Integer, ForeignKey("persona.id"))

    tipousuario = db.relationship("Tipousuario")
    persona = db.relationship("Persona")
    

class Persona(db.Model):
    __tablename__ = 'persona'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    idTipodni = db.Column(db.Integer, ForeignKey("tipodni.id"), nullable=False)
    dni = db.Column(db.String(20), nullable=False, unique=True)
    direccion = db.Column(db.String(50), nullable=False)
    idLocalidad = db.Column(db.Integer, ForeignKey("localidad.id"), nullable=False)
    idPais = db.Column(db.Integer, ForeignKey("pais.id"), nullable=False)
    fechaNacimiento = db.Column(db.String(50), nullable=False)
    idSexo = db.Column(db.Integer, ForeignKey("sexo.id"), nullable=False)
    telefono = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    fechaCarga = db.Column(db.String(50), nullable=False)
    activo = db.Column(db.Boolean(), nullable=False)

    tipodni = db.relationship("Tipodni")
    localidad = db.relationship("Localidad")
    pais = db.relationship("Pais")
    sexo = db.relationship("Sexo")



# -------------------- Serializaciones ---------------

class PaisSerializer(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()


class PaisSinIdSerializer(ma.Schema):
    nombre = fields.String()


class PersonaSerializer(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    idTipodni = fields.Integer()
    dni =  fields.String()
    direccion = fields.String()
    idLocalidad = fields.Integer()
    idPais = fields.Integer()
    # quiere decir que no traiga el id de pais
    # pais = fields.Nested(PaisSerializer, exclude=['id',])
    fechaNacimiento = fields.String()
    idSexo = fields.Integer()
    telefono = fields.String()
    email = fields.String()
    fechaCarga = fields.String()
    activo = fields.Boolean()


class ProvinciaSerializer(ma.Schema):
        id = fields.Integer(dump_only=True)
        nombre = fields.String()
        idPais = fields.Integer()


class LocalidadSerializer(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    idProvincia = fields.Integer()


class SexoSerializer(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()


class TipoDniSerializer(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()


class UsuarioSerializer(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    contrasenia = fields.String()
    idTipousuario = fields.Integer()
    fechaCarga = fields.String()
    idPersona = fields.Integer()


class TipoUsuarioSerializer(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    descripcion = fields.String()







# ------ RUTAS --------
@app.route('/paises')
def get_paises():
    pais = db.session.query(Pais).all()
    pais_schema = PaisSerializer().dump(pais, many=True)
    return jsonify(pais_schema)


@app.route('/nombre_paises')
def get_nombre_paises():
    pais = db.session.query(Pais).all()
    pais_schema = PaisSinIdSerializer().dump(pais, many=True)
    return jsonify(pais_schema)


@app.route('/personas')
def persona():
    persona = db.session.query(Persona).all()
    persona_schema = PersonaSerializer().dump(persona, many=True)
    return jsonify(persona_schema)


@app.route('/provincias')
def provincia():
    provincia = db.session.query(Provincia).all()
    provincia_schema = ProvinciaSerializer().dump(provincia, many=True)
    return jsonify(provincia_schema)


@app.route('/localidades')
def localidad():
    localidad = db.session.query(Localidad).all()
    localidad_schema = LocalidadSerializer().dump(localidad, many=True)
    return jsonify(localidad_schema)


@app.route('/sexos')
def sexo():
    sexo = db.session.query(Sexo).all()
    sexo_schema = SexoSerializer().dump(sexo, many=True)
    return jsonify(sexo_schema)


@app.route('/tipos_dni')
def tipoDni():
    tipodni = db.session.query(TipoDni).all()
    tipodni_schema = TipoDniSerializer().dump(tipodni, many=True)
    return jsonify(tipodni_schema)


@app.route('/usuarios')
def usuario():
    usuario = db.session.query(Usuario).all()
    usuario_schema = UsuarioSerializer().dump(usuario, many=True)
    return jsonify(usuario_schema)


@app.route('/tipos_usuario')
def tipoUsuario():
    tipousuario = db.session.query(Tipousuario).all()
    tipousuario_schema = TipoUsuarioSerializer().dump(tipousuario, many=True)
    return jsonify(tipousuario_schema)




if __name__ == '__main__':
    app.run(debug=True)