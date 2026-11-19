from database import db

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_categoria = db.Column(db.String(50), unique=True, nullable=False)
    produtos = db.relationship('Produto', backref='categoria', lazy=True)


class Produto(db.Model):
    __tablename__ = 'produto'

    # Campos renomeados para bater com o index.html (p.id, p.nome, p.imagem)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    imagem = db.Column(db.String(255), nullable=False, default='padrao.png')
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False, default=1)