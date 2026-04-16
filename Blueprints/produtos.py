from flask import Flask, render_template, request, url_for, session, redirect, Blueprint, abort
from flask_login import login_required, login_user, logout_user, current_user
from db import db
from models import Loja, Produtos, Categoria

prod_bp = Blueprint("prod", __name__)

# Página de produtos
   
@prod_bp.route("/produtos/<loja>", methods=["GET", "POST"])
def produtos(loja):    
    loja_obj = Loja.query.filter_by(username=loja).first()
    
    if not loja_obj:
        abort(404)
    
    produtos = loja_obj.produtos
    
    return render_template(
      "produtos/produtos.html", 
      loja=loja_obj, 
      produtos=produtos
      )
    
# Adicionar produtos

@prod_bp.route("/produtos/add",  methods=["POST"])
@login_required
def addprodutos():
    addnome = request.form.get("nomeProdutoAdd", "").strip()
    addpreco = request.form.get("precoProdutoAdd")        
    addquant = request.form.get("quantProdutoAdd")                
    addmostrar = request.form.get("mostrarProdutoAdd") == "Sim"
    categoria_id = request.form.get("categoria_id")
 
    if not addnome:
        return "Nome do produto obrigatório", 400        
    addpreco = float(addpreco) if addpreco else 0
    addquant = int(addquant) if addquant else 0
    categoria_id = int(categoria_id) if categoria_id else None
    
    produto_novo = Produtos(
    nome=addnome, 
    preco=addpreco, 
    quantidade=addquant, 
    mostrar=addmostrar, 
    loja_id=current_user.id,
    categoria_id=categoria_id
        )
        
    db.session.add(produto_novo)
    db.session.commit()
        
    return redirect(url_for("prod.produtos", loja=current_user.username))
    
# Editar produtos

@prod_bp.route("/produtos/edit", methods=["GET", "POST"])
@login_required
def editprodutos():
    produtos = Produtos.query.filter_by(loja_id=current_user.id).all()
    
    categorias = Categoria.query.filter_by(loja_id=current_user.id).all()
    mostrar_input_categoria = request.args.get("nova_categoria") == "1"
    
    if request.method == "POST":

        for produto in produtos:
          
          #Excluir produto
          
            deletar_produto = request.form.get(f"delproduto_{produto.id}")
            
            if deletar_produto == "excluir produto":
                db.session.delete(produto)
                continue
                
          #Editar
          
            nome = request.form.get(f"nomeProduto_{produto.id}", "").strip()
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
        return redirect(url_for("prod.produtos", loja=current_user.username))
        
    return render_template(
      "produtos/edit_produtos.html", 
      produtos=produtos,
      categorias=categorias, 
      mostrar_input_categoria=mostrar_input_categoria
      )

# ============= Categorias ==============

# Criar categoria

@prod_bp.route("/addcategoria", methods=["POST"])
@login_required
def addcategoria():
  nome = request.form.get("nomeCategoriaForm").strip()
  
  if not nome:
    return "Nome da categoria obrigatório", 400
  categoria_nova = Categoria(nome=nome, loja_id=current_user.id)
  
  db.session.add(categoria_nova)
  db.session.commit()
  return redirect(url_for("prod.editprodutos"))