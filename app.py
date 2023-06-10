from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


# Definir modelo de la tabla "posteos"
class Posteo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    titulo = db.Column(db.String(100))
    texto = db.Column(db.String(1000))


# Ruta de inicio o bienvenida
@app.route('/')
def index():
    return render_template('blog.html')


# Ruta de login
@app.route('/login')
def login():
    return render_template('login.html')


# Endpoint para obtener los últimos tres posteos de un usuario
@app.route('/posteos/', methods=['GET', 'POST'])
def posteos():
    if request.method == 'GET':
        usuario = request.args.get('usuario')
        posteos = Posteo.query.filter_by(usuario=usuario).order_by(Posteo.id.desc()).limit(3).all()
        datos = []
        for posteo in posteos:
            datos.append({'titulo': posteo.titulo, 'texto': posteo.texto})
        return jsonify(datos)
    elif request.method == 'POST':
        usuario = request.form['usuario']
        titulo = request.form['titulo']
        texto = request.form['texto']
        posteo = Posteo(usuario=usuario, titulo=titulo, texto=texto)
        db.session.add(posteo)
        db.session.commit()
        return Response(status=201)


# Endpoint para eliminar todos los posteos de un usuario
@app.route('/posteos/<usuario>', methods=['DELETE'])
def eliminar_posteos(usuario):
    Posteo.query.filter_by(usuario=usuario).delete()
    db.session.commit()
    return Response(status=200)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Base de datos generada")
    app.run(host="127.0.0.1", port=5000)
