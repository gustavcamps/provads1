import os
from flask import Flask
from database import db
from models import Categoria

app = Flask(__name__)

# Configurações da aplicação
app.config['SECRET_KEY'] = 'chave_secreta_loja'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///provafinal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do diretório de uploads
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Garante que a pasta static/uploads exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Inicialização do Banco de Dados
db.init_app(app)

# Criação das tabelas e dados iniciais
with app.app_context():
    db.create_all()

    if not Categoria.query.first():
        categorias_iniciais = [
            Categoria(nome_categoria='Eletrônicos'),
            Categoria(nome_categoria='Informática'),
            Categoria(nome_categoria='Acessórios'),
        ]
        db.session.add_all(categorias_iniciais)
        db.session.commit()

# Importa as rotas após inicializar o app e o db
from routes import *

if __name__ == '__main__':
    app.run(debug=True)