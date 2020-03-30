from flasksystem import ma
from flasksystem.models import Reactivo, Materia, User, Quimico, HistorialReactivos, HistorialMaterias, HistorialQuimicos
from marshmallow import ValidationError, validates_schema


def validate_positive(num):
    if num < 0:
        raise ValidationError('El numero debe ser positivo')


# Schema
class ReactivoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reactivo
    
    id = ma.auto_field()
    nombre = ma.auto_field()
    codigo = ma.auto_field()
    bajo_stock = ma.auto_field(validate=validate_positive)
    area = ma.auto_field()
    cantidad = ma.auto_field(validate=validate_positive)
    medida = ma.auto_field()
    
class MateriaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Materia
        load_instance = True
        # include_fk = True

    id = ma.auto_field()
    nombre = ma.auto_field()
    codigo = ma.auto_field()
    bajo_stock = ma.auto_field(validate=validate_positive)
    area = ma.auto_field()
    cantidad = ma.auto_field(validate=validate_positive)
    medida = ma.auto_field()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

class QuimicoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quimico
        include_relationships = True

class HistorialReactivosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistorialReactivos
        include_relationships = True

class HistorialMateriasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistorialMaterias
        include_relationships = True

class HistorialQuimicosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistorialQuimicos
        include_relationships = True

class MateriaBajoStockSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Materia
        load_instance = True
        # include_fk = True

    bajo_stock = ma.auto_field(validate=validate_positive)


# Init Schema

reactivo_schema = ReactivoSchema()
reactivos_schema = ReactivoSchema(many=True)

materia_schema = MateriaSchema()
materia_bajo_stock_schema = MateriaBajoStockSchema()
materias_schema = MateriaSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

quimico_schema = QuimicoSchema()
quimicos_schema = QuimicoSchema(many=True)

historial_reactivo_schema = HistorialReactivosSchema()
historiales_reactivo_schema = HistorialReactivosSchema(many=True)

historial_materia_schema = HistorialMateriasSchema()
historiales_materia_schema = HistorialMateriasSchema(many=True)

historial_quimico_schema = HistorialQuimicosSchema()
historiales_quimico_schema = HistorialQuimicosSchema(many=True)
