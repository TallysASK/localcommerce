from flask import Flask, render_template, request, url_for, session, redirect, Blueprint, abort
from flask_login import login_required, login_user, logout_user, current_user
from db import db
from models import Loja, Produtos

store_bp = Blueprint("store", __name__)

# Perfil loja

@store_bp.route("/store/<username>")
def store(username):
    loja = Loja.query.filter_by(username=username).first()
    
    if not loja:
        return abort(404)   
         
    produtos = loja.produtos
    
    return render_template("store/store.html", loja=loja, produtos = produtos)

# Editar perfil loja   

@store_bp.route("/store/edit", methods=["GET" , "POST"])
@login_required
def editstore():
    
    if request.method == "POST":
        novo_viewname = request.form.get("nomeLj")
        descricao = request.form.get("descricaoLj")
        
        if not novo_viewname:
            novo_viewname = current_user.username
        if not descricao:
            descricao = "descrição"
            
        current_user.viewname = novo_viewname
        current_user.descricao = descricao
        db.session.commit()
        
        return redirect(url_for("store.store", username=current_user.username))
    
    return render_template("store/edit_store.html")

# Produtos
   
@store_bp.route("/produtos/<loja>", methods=["GET", "POST"])
def produtos(loja):    
    loja_obj = Loja.query.filter_by(username=loja).first()
    
    if not loja_obj:
        abort(404)
        
    produtos = loja_obj.produtos
    
    return render_template("store/produtos.html", loja=loja_obj, produtos=produtos)

# Editar produtos

@store_bp.route("/produtos/edit", methods=["GET", "POST"])
@login_required
def editprodutos():
    produtos = Produtos.query.filter_by(loja_id=current_user.id)

    if request.method == "POST":

        for produto in produtos:

            nome = request.form.get(f"nomeProduto_{produto.id}").strip()
            preco = request.form.get(f"precoProduto_{produto.id}")
            quant = request.form.get(f"quantProduto_{produto.id}")
            mostrar = request.form.get(f"mostrarProduto_{produto.id}")

            if nome:
                produto.nome = nome

            if preco:
                produto.preco = float(preco)

            if quant:
                produto.quantidade = int(quant)
                
            if mostrar is not None:
                produto.mostrar = (mostrar == "Sim")

        db.session.commit()
        return redirect(url_for("store.produtos", loja=current_user.username))
        
    return render_template("store/edit_produtos.html", produtos=produtos)
    
# Adicionar produtos

@store_bp.route("/produtos/add",  methods=["POST"])
@login_required
def addprodutos():
    addnome = request.form.get("nomeProdutoAdd").strip()
    addpreco = request.form.get("precoProdutoAdd")        
    addquant = request.form.get("quantProdutoAdd")                
    addmostrar = request.form.get("mostrarProdutoAdd") == "Sim"
 
    if not addnome:
        return "Nome do produto obrigatório", 400        
    addpreco = float(addpreco) if addpreco else 0
    addquant = int(addquant) if addquant else 0
        
    produto_novo = Produtos(
    nome=addnome, 
    preco=addpreco, 
    quantidade=addquant, 
    mostrar=addmostrar, loja_id=current_user.id
        )
        
    db.session.add(produto_novo)
    db.session.commit()
        
    return redirect(url_for("store.produtos", loja=current_user.username))