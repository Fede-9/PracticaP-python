import json
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, DateTime
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/matias'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.name
    
    def __init__(self, name):
        self.name = name


class Province(db.Model):
    __tablename__ = 'province'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    idContry =db.Column(db.Integer, ForeignKey('country.id'))


class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    idProvince = db.Column(db.Integer, ForeignKey('province.id'))


class Sex(db.Model):
    __tablename__ = 'sex'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=True)


class DniType(db.Model):
    __tablename__ = 'dniType'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=True)


class Person(db.Model):
    __tablename__='person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    idTypeDni = db.Column(db.Integer, ForeignKey('dniType.id'))
    dni = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(100), nullable=True)
    idLocation = db.Column(db.Integer, ForeignKey('location.id'))
    idCountry = db.Column(db.Integer, ForeignKey('country.id'))
    born = db.Column(db.TIMESTAMP, nullable=True)
    idSex = db.Column(db.Integer, ForeignKey('sex.id'))
    phone = db.Column(db.Integer, nullable=False)
    mail = db.Column(db.String(50), nullable=False)
    uploadDate = db.Column(db.TIMESTAMP, nullable=True)
    active = db.Column(db.Boolean, nullable=True, default=True)
    countries = db.relationship('Country')


class UserType(db.Model):
    __tablename__ = 'userType'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=True)


class User(db.Model):
    __tablename__='user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=True)
    idUserType = db.Column(db.Integer, ForeignKey('userType.id'))
    fCarga = db.Column(db.TIMESTAMP, nullable=True)
    idPerson = db.Column(db.Integer, ForeignKey('person.id'))


# Serializadores 
class CountrySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class CountryWithoutIdSchema(ma.Schema):
    name = fields.String()


class ProvinceSchema(ma.Schema):
    name = fields.String()
    idCountry = fields.Integer()


class PersonSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    idTypeDni = fields.Integer()
    dni = fields.Integer()
    address = fields.String()
    idLocation = fields.Integer()
    idCountry = fields.Integer()
    countries = fields.Nested(CountrySchema, exclude=['id',])
    born = fields.String()
    idSex = fields.Integer()
    phone = fields.Integer()
    mail = fields.String()
    uploadDate = fields.Date()
    active = fields.Boolean()

# SI NO LE DETERMINO EL METODO; SIEMPRE ES UN GET
@app.route('/countries')
def get_countries():
    country = db.session.query(Country).all()    
    countrie_schema = CountrySchema().dump(country, many=True)
    return jsonify(countrie_schema)

# POST
@app.route('/countries', methods=['POST'])
def add_countrie():
    if request.method == 'POST':
        data = request.json
        name = data['name']
        countries = db.session.query(Country).all()
        for country in countries:
            if name == country.name:
                return jsonify({"Mensaje":"Ya existe un pais con ese nombre"}),404
        new_countrie = Country(name=name)
        db.session.add(new_countrie)
        db.session.commit()
        countrie_schema = CountryWithoutIdSchema().dump(
           new_countrie
        )
        return jsonify(
            {"Mensaje":"El pais se creo correctamente"},
            {"Pais": countrie_schema}
        ), 201
        

@app.route('/countries_names')
def get_country_names():
    
    countrie_schema = CountryWithoutIdSchema().dump(
        db.session.query(Country).all(), many=True
    )
    return jsonify(countrie_schema)

@app.route('/persons')
def get_persons():
    persons = db.session.query(Person).all()
    persons_schema = PersonSchema().dump(persons, many=True)
    return jsonify(persons_schema)

@app.route('/users')
def get_users():
    users = db.session.query(User).all()
    if len(users) == 0:
        return jsonify({'Mensaje':'No existen usuario aun'}),201
    return jsonify({'Tenemos tenemos usuario'}), 
    
@app.route('/provinces')
def get_provinces():
    provinces = db.session.query(Province).all()
    provice_shemma = ProvinceSchema().dump(provinces, many=True)
    return jsonify(provice_shemma)

@app.route('/provinces', methods=['post'])
def add_province():
    if request.method == 'POST':
        data = request.json
        name = data['name']
        country_id = data['country_id']
        try:
            new_province = Province(idContry=country_id, name=name)
            db.session.add(new_province)
            db.session.commit()
            
            provice_schema = ProvinceSchema().dump(new_province)

            return jsonify(
                {"Mensaje":"La Provincia se creo correctamente"},
                {"Pais": provice_schema}
            ), 201

        except:
            return jsonify(
                {"Mensaje": "Algo salio mal, valide los datos"},
            ), 404

if __name__ == '__main':
  app.run(debug=True)


