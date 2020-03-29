from flasksystem import ma
from flasksystem.models import Reactivo, Materia, User, Quimico, HistorialReactivos, HistorialMaterias, HistorialQuimicos

# Schema

class ReactivoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'codigo', 'medida', 'bajo_stock', 'area', 'cantidad')

class MateriaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'codigo', 'medida', 'bajo_stock', 'area', 'cantidad')

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class QuimicoSchema(ma.ModelSchema):
    class Meta:
        model = Quimico

class HistorialReactivosSchema(ma.ModelSchema):
    class Meta:
        model = HistorialReactivos

class HistorialMateriasSchema(ma.ModelSchema):
    class Meta:
        model = HistorialMaterias

class HistorialQuimicosSchema(ma.ModelSchema):
    class Meta:
        model = HistorialQuimicos

# Init Schema

reactivo_schema = ReactivoSchema()
reactivos_schema = ReactivoSchema(many=True)

materia_schema = MateriaSchema()
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
