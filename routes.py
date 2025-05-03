import os
from flask import jsonify, redirect, render_template, request, session
from flask_login import login_user
from app import ALLOWED_EXTENSIONS
from config import app, db
from models.Produit import Produit
from models.User import User
from models.enums.Role import Role
from templates.FormType.productForm import ProductForm
from werkzeug.utils import secure_filename

@app.route("/usercreate")
def usercreate():
        new_user = User(username="booba", email="booba@example.com", password="password1", role=Role.ADMIN)
        db.session.add(new_user)
        db.session.commit()
        return render_template("Home/index.html",products=Produit.query.all())

@app.route("/")
def home():
        return render_template("Home/index.html",products=Produit.query.all())

@app.route("/about") 
def about():
        return render_template("About/index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password=password).first()
        if user :
            login_user(user)
            return redirect("/")
    return render_template("shared/login.html")

@app.route("/search/<search>")
def search(search):
    # Récupérer les produits qui correspondent à la recherche
    products = Produit.query.filter(Produit.name.ilike("%" + search + "%")).all()
    # Convertir les produits en JSON
    data = [{"id": p.id, "name": p.name ,"description": p.description, "price": p.price, "qte": p.qte, "image": p.image} for p in products]
    # Retourner les données en JSON
    return jsonify(data)

@app.route("/service")
def service():
        return render_template("Service/index.html")


def ajouterProduit(produit,qte):
    # Crée le panier dans la session s'il n'existe pas
    if "cart" not in session:
        session["cart"] = []
    
    # Ajoute le produit au panier
    produitserialized = produit.serialize()
    #Parcourir dans la session pour voir si le produit est deja dans le panier
    produit_existe = False
    for detail_commande in session["cart"]:
        if detail_commande["produit_id"] == produitserialized.get("id"):
            detail_commande["qte"] += qte
            produit_existe = True
            detail_commande["total"] = produitserialized.get("price")*detail_commande["qte"]
            break

    if not produit_existe:
        detail_commande = DetailCommande(
            commande_id=None,
            produit_id=produitserialized.get("id"),
            qte=qte,
            total=produitserialized.get("price")*qte
        )
        session["cart"].append(detail_commande.serialize())

    session.modified = True  # Indique à Flask que la session a changé
  


   
@app.route("/add_product",)
def add_product():
        form=ProductForm()
        return render_template("Home/form.html",form=form)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = ProductForm()
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        produit=Produit(form.name.data,form.description.data,form.price.data,form.qte.data,filename)
        db.session.add(produit)
        db.session.commit()
        return render_template("Home/index.html",products=Produit.query.all())
    return render_template('Home/form.html', form=form)


# //page details produit
@app.route("/product/<int:id>")
def product(id):
    product = Produit.query.get(id)
    return render_template("Home/detail.html",product=product)


# Supprimer un produit
@app.route("/delete/<int:id>")
def delete(id):
    produit = Produit.query.get(id)
    db.session.delete(produit)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>")
def edit(id):
    produit = Produit.query.get(id)
    form = ProductForm(obj=produit)
    return render_template("Home/update.html",form=form,id=id,produit=produit)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    produit = Produit.query.get(id)
    form = ProductForm(obj=produit)
    if form.validate_on_submit():
        filename = produit.image
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        produit.name = form.name.data
        produit.description = form.description.data
        produit.price = form.price.data
        produit.qte = form.qte.data
        produit.image = filename
        db.session.commit()
        return redirect("/")
    return render_template("Home/update.html",form=form)


@app.route("/logout")
def logout():
    return redirect("/login")