import os
import uuid
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app
from database import db
from models import Categoria, Produto

EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def extensao_valida(nome_arquivo):
    return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

def remover_imagem_disco(nome_arquivo):
    if nome_arquivo and nome_arquivo != 'padrao.png':
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        if os.path.exists(caminho):
            os.remove(caminho)


@app.route('/')
def index():
    # Filtro de busca por nome ordenado alfabeticamente
    busca = request.args.get('busca', '').strip()
    if busca:
        produtos = Produto.query.filter(Produto.nome.ilike(f'%{busca}%')).order_by(Produto.nome.asc()).all()
    else:
        produtos = Produto.query.order_by(Produto.nome.asc()).all()

    categorias = Categoria.query.order_by(Categoria.nome_categoria.asc()).all()
    return render_template('index.html', produtos=produtos, categorias=categorias, busca=busca)


# Rota /salvar exigida pelo seu index.html
@app.route('/salvar', methods=['POST'])
def salvar():
    nome = request.form.get('nome', '').strip()
    preco_str = request.form.get('preco', '').strip().replace(',', '.')
    arquivo = request.files.get('foto')

    # Validações exigidas pelo PDF
    if len(nome) < 3:
        flash('Erro: O nome do produto deve ter pelo menos 3 caracteres.', 'danger')
        return redirect(url_for('index'))

    try:
        preco = float(preco_str)
        if preco <= 0:
            flash('Erro: O preço deve ser maior que zero.', 'danger')
            return redirect(url_for('index'))
    except ValueError:
        flash('Erro: Informe um valor numérico válido para o preço.', 'danger')
        return redirect(url_for('index'))

    nome_foto = 'padrao.png'
    if arquivo and arquivo.filename != '':
        if not extensao_valida(arquivo.filename):
            flash('Erro: Extensão de imagem não permitida.', 'danger')
            return redirect(url_for('index'))
        
        ext = arquivo.filename.rsplit('.', 1)[1].lower()
        nome_seguro = secure_filename(arquivo.filename.rsplit('.', 1)[0])
        nome_foto = f"{nome_seguro}_{uuid.uuid4().hex[:8]}.{ext}"
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_foto))

    # Pega a primeira categoria por padrão caso o index não envie o select
    primeira_categoria = Categoria.query.first()
    id_cat = primeira_categoria.id_categoria if primeira_categoria else 1

    novo_produto = Produto(
        nome=nome,
        preco=preco,
        imagem=nome_foto,
        id_categoria=id_cat
    )
    db.session.add(novo_produto)
    db.session.commit()
    flash('Produto cadastrado com sucesso!', 'success')
    return redirect(url_for('index'))


@app.route('/excluir/<int:id>')
def excluir(id):
    produto = Produto.query.get_or_404(id)
    remover_imagem_disco(produto.imagem)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('index'))