from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename 
import os

# Declarando nombre de la aplicación e inicializando
app = Flask(__name__)

# Configuración del directorio de subida y descarga
UPLOAD_FOLDER = 'static/archivos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return 'Ruta no encontrada'

# Creando un Decorador
@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = request.args.get('search', '')  # Obtener el término de búsqueda de los parámetros de la URL
    archivos = os.listdir(app.config['UPLOAD_FOLDER'])

    if search_query:
        archivos = [archivo for archivo in archivos if search_query.lower() in archivo.lower()]

    return render_template('index.html', archivos=archivos, search_query=search_query)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    return render_template('inicio.html')

@app.route('/TIC', methods=['GET', 'POST'])
def tic():
    return render_template('TIC.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/registrar-archivo', methods=['GET', 'POST'])
def registarArchivo():
    archivo_subido = None
    if request.method == 'POST':
        # Script para archivo
        file = request.files['archivo']
        basepath = os.path.dirname(__file__) # La ruta donde se encuentra el archivo actual
        filename = secure_filename(file.filename) # Nombre original del archivo
        
        upload_path = os.path.join(basepath, app.config['UPLOAD_FOLDER'], filename) 
        file.save(upload_path)
        archivo_subido = filename
        
    archivos = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', archivos=archivos, archivo_subido=archivo_subido)

# Nueva ruta para descargar archivos
@app.route('/descargar-archivo/<filename>', methods=['GET'])
def descargarArchivo(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return 'Archivo no encontrado', 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
