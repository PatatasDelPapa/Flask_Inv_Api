from flask import Blueprint, render_template, jsonify

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(403)
def error_403(error):
    return jsonify({'error': 'No tienes permisos para hacer esto'}), 403

@errors.app_errorhandler(404)
def error_404(error):
    return jsonify({'error': 'Pagina no encontrada'}), 404

@errors.app_errorhandler(405)
def error_405(error):
    return jsonify({'error': 'Metodo no permitido'}), 405

@errors.app_errorhandler(500)
def error_500(error):
    return jsonify({'error': 'Algo salio mal'}), 500
