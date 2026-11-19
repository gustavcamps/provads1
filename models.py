from database import db

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_categoria = db.Column(db.String(50), unique=True, nullable=False)


class Produto(db.Model):
    __tablename__ = 'produto'

    id_produto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    foto = db.Column(db.String(255), nullable=False, default='padrao_produto.png')
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)