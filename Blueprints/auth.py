from flask import Flask, render_template, request, url_for, session, redirect, Blueprint, abort
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import Loja, Produtos

auth_bp = Blueprint("auth", __name__)

#Cadastro

@auth_bp.route("/cadastro", methods=["GET" , "POST"])
def cadastro():
   
   if request.method == "GET":
       return render_template("auth/cadastro.html")
       
   if request.method == "POST":
        nome = request.form["nomeCadastro"]
        senha = request.form["senhaCadastro"]
        
        verificar_nome = Loja.query.filter_by(username=nome).first()
        
        if verificar_nome:
            abort(404)
        
        else:  
            senha_hash = generate_password_hash(senha)
            
            nova_loja = Loja(username=nome, senha=senha_hash, viewname=nome, descricao="descrição")
        
            db.session.add(nova_loja)
            db.session.commit()
            login_user(nova_loja)
                
            return redirect(url_for("store.editstore"))       
  
 # Login
       
@auth_bp.route("/login", methods=["GET" , "POST"])
def login():
    
    if request.method == "POST":
        nome_digit = request.form["nomeLogin"]
        senha_digit = request.form["senhaLogin"]
        
        user = Loja.query.filter_by(username=nome_digit).first()
        
        if user and check_password_hash(user.senha , senha_digit):
            login_user(user)
        
            return redirect(url_for("home"))
            
    return render_template("auth/login.html")

# Logout
        
@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout = request.form.get("logout")
    if logout:
        logout_user()
        
    return redirect(url_for("home"))

# Deletar conta
    
@auth_bp.route("/delconta", methods=["POST"])
@login_required
def delconta():
    
    conta = Loja.query.filter_by(id=current_user.id).first()
    
    produtos = Produtos.query.filter_by(loja_id=current_user.id).all()
    
    delete_conta = request.form.get("delconta")
    if delete_conta == "deletar":
        db.session.delete(conta)
        
        for produto in produtos:
            db.session.delete(produto)
        
        db.session.commit()
        
    return redirect(url_for("home"))