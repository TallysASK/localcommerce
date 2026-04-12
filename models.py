from db import db
from flask_login import UserMixin

# Usuario
class Loja(db.Model, UserMixin):
    
    id = db.Column(db.Integer , primary_key=True)
    
    username = db.Column(db.String(40) , unique=True , nullable=False)
    
    senha = db.Column(db.String(40) , nullable=False)
    
    viewname = db.Column(db.String(40))

    descricao = db.Column(db.String(100))
    
    # logo, banner e email
        
    produtos = db.relationship("Produtos" , backref="loja" , lazy=True)

# Produtos
class Produtos(db.Model):
    
    id = db.Column(db.Integer , primary_key=True)
    
    nome = db.Column(db.String(40) , nullable=False)
    
    quantidade = db.Column(db.Integer)
    
    preco = db.Column(db.Float)
    
    mostrar = db.Column(db.Boolean , default=True)
    
    #imagem
    
    loja_id = db.Column(db.Integer , db.ForeignKey("loja.id"))
    
# class Categoria