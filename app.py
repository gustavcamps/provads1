import os
from flask import Flask
from database import db
from models import Usuario, Cliente, Barbeiro, Servico, Agendamento
from routes import agendamentos_bp
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

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

# Registro das rotas
app.register_blueprint(agendamentos_bp)

# Criação das tabelas e dados iniciais
with app.app_context():
    db.create_all()

    if not Categoria.query.first():
        Categoria = [
            categoria(nome_categoria='Eletrônicos'),
            categoria(nome_categoria='Informática'),
            categoria(nome_categoria='Acessórios'),
        ]
        db.session.add_all(barbeiros_iniciais)

    if not Servico.query.first():
        servicos_iniciais = [
            Servico(nome_do_servico='Corte Masculino', preco=35.00),
            Servico(nome_do_servico='Barba Completa', preco=25.00),
            Servico(nome_do_servico='Cabelo + Barba', preco=55.00)
        ]
        db.session.add_all(servicos_iniciais)

    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)