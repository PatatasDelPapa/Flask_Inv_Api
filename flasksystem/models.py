import enum
from datetime import datetime
from flasksystem import db, login_manager, ma
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Area(enum.Enum):
    Lab = 'Lab'
    Bod = 'Bod'
    Lab_Bod = 'Lab_Bod'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        item = cls(item) \
               if not isinstance(item, cls) \
               else item  # a ValueError thrown if item is not defined in cls.
        return item.value

class Medida(enum.Enum):
    Gramos = 'Gramos'
    Kilogramos = 'Kilogramos'
    Ml = 'Ml'
    Unidad = 'Unidad'
    Litros = 'Litros'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        item = cls(item) \
               if not isinstance(item, cls) \
               else item  # a ValueError thrown if item is not defined in cls.
        return item.value

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reactivos = db.relationship('HistorialReactivos', backref='user', lazy=True)
    materias = db.relationship('HistorialMaterias', backref='user', lazy=True)
    area = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.area.value}')"

class Quimico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    reactivo_id = db.Column(db.Integer, db.ForeignKey('reactivo.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    area = db.Column(db.String(15), nullable=False)

class Reactivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(30), nullable=False)
    medida = db.Column(db.String(20), nullable=False)
    historial = db.relationship('HistorialReactivos', backref='reactivo', lazy=True)
    quimico = db.relationship('Quimico', backref='reactivo', lazy=True)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    bajo_stock = db.Column(db.Integer, nullable=False, default=0)
    tipo = db.Column(db.String(20), nullable=False, default='Reactivo')
    formula = db.relationship('Formula', uselist=False, back_populates='reactivo') #Acceso a los datos de la tabla Formula
    area = db.Column(db.String(15), nullable=False)
    tiene_formula = db.Column(db.Boolean, nullable=False, default=False)
    
    # def __init__(self, nombre, codigo, medida, bajo_stock, area):
    #     self.nombre = nombre
    #     self.codigo = codigo
    #     self.medida = medida
    #     self.bajo_stock = bajo_stock
    #     self.area = area

    def __repr__(self):
        return f"Reactivo('{self.nombre}', '{self.codigo}', '{self.medida}', '{self.area}')"

class HistorialReactivos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    observacion = db.Column(db.String(100), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reactivo_id = db.Column(db.Integer, db.ForeignKey('reactivo.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    historial_quimico = db.relationship('HistorialQuimicos', backref='historial_reactivo', lazy=True)
    lote = db.Column(db.String(20))
    area = db.Column(db.String(15), nullable=False)

class Ingrediente(db.Model):
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'), primary_key=True)
    formula_id = db.Column(db.Integer, db.ForeignKey('formula.id'), primary_key=True)
    ratio = db.Column(db.DECIMAL, nullable=False)
    materia = db.relationship('Materia', back_populates='formulas', passive_deletes='all') #Acceso a los datos de la tabla Materia
    formula = db.relationship('Formula', back_populates='materias', passive_deletes='all') #Acceso a los datos de la tabla Formula

class BodCorr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nro = db.Column(db.Integer, nullable=False, default=1)

class LabCorr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nro = db.Column(db.Integer, nullable=False, default=1)

# Cambiar BODCORR Y LABCORR A UN SOLO CORRELATIVO (QUIZAS ELEJIR UN MEJOR NOMBRE)
# class Correlativo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nro = db.Column(db.Integer, nullable=False, default=1)

class Formula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reactivo_id = db.Column(db.Integer, db.ForeignKey('reactivo.id'))
    reactivo = db.relationship('Reactivo', back_populates='formula') # Accso a los datos de la tabla Reactivo
    materias = db.relationship('Ingrediente', back_populates='formula') # Acceso a los datos de la tabla Ingrediente

    def __repr__(self):
        return f"Formula('{self.id}')"


class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(30), nullable=False)
    medida = db.Column(db.String(20), nullable=False)
    historial = db.relationship('HistorialMaterias', backref='materia', lazy=True)
    quimico = db.relationship('Quimico', backref='materia', lazy=True)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    bajo_stock = db.Column(db.Integer, nullable=False, default=0)
    tipo = db.Column(db.String(20), nullable=False, default='Materia')
    formulas = db.relationship('Ingrediente', back_populates='materia') #Acceso a los datos de la tabla Ingredientes
    area = db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return f"Materia Prima('{self.nombre}', '{self.codigo}', '{self.medida}', '{self.area}')"

class HistorialMaterias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    observacion = db.Column(db.String(100), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False) 
    historial_quimico = db.relationship('HistorialQuimicos', backref='historial_materia', lazy=True)
    area = db.Column(db.String(15), nullable=False)

class HistorialQuimicos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    reactivo_id = db.Column(db.Integer, db.ForeignKey('historial_reactivos.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('historial_materias.id'))
    fecha_registro = db.Column(db.DateTime, nullable=False)
    area = db.Columndb.String(15), nullable=False)


# Schema
class ReactivoSchema(ma.ModelSchema):
    class Meta:
        model = Reactivo

class MateriaSchema(ma.ModelSchema):
    class Meta:
        model = Materia

# Init Schema
