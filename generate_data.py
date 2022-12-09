import os

os.system("rm db.sqlite")
os.system("rm exercice.sqlite")

"""
Ce fichier sert à générer des informations fictives avec le module "Faker"
Il nous permets de générer des lignes SQL en fonction des besoins de projet
"""

from conf import * # On importe notre configuration de Table
from faker import Faker
import random
from faker_food import FoodProvider

fake = Faker("FR") # On utilise les formats FR de faker pour générer les données
fake.add_provider(FoodProvider)
fake.seed_instance(0) # On définis une seed pour que l'aléatoire soit figé durant nos tests


def generateCountry(nb_country: int):
    """
    Fonction qui genere des pays dans la BDD
    : param nb_country int : Nombre de pays à générer
    """
    for _ in range(0, nb_country):
        pays = Pays(pays=fake.unique.country())
        session1.add(pays)

    session1.commit()

generateCountry(225)

def generateRestaurant(nb_restaurant):
    """
    Fonction qui genere des restaurants dans la BDD
    : param nb_country int : Nombre de pays à générer
    """

    for _ in range(0, nb_restaurant):
        my_country = random.choice(session1.query(Pays).all()).pays
        code = fake.unique.postcode()
        resto = Restaurant(code_postal=code,departement=code[:2], pays=my_country, capacite=fake.pyint(min_value=50, max_value=200), espace_enfant=fake.pyint(min_value=0, max_value=1), service_rapide=fake.pyint(min_value=0, max_value=1), accessibilite=fake.pyint(min_value=0, max_value=1), parking=fake.pyint(min_value=0, max_value=1))
        session1.add(resto)
        
    session1.commit()

generateRestaurant(1000)

def generateEmploye(max_manager: int, max_employe: int):
    """
    Fonction qui genere les employés de chaques Restaurant
    """

    for r in session1.query(Restaurant).all():
        session1.add(Employe(code_postal=r.code_postal, poste="Directeur", nom=fake.last_name(), experience=fake.pyint(min_value=1, max_value=5), note=fake.pyint(min_value=1, max_value=10), adresse=fake.street_address()))
        for _ in range(0, fake.pyint(min_value=1, max_value=max_manager)):
            session1.add(Employe(code_postal=r.code_postal, poste="Manager", id_superieur=session1.query(Employe).filter_by(code_postal = r.code_postal).first().id_employe, nom=fake.last_name(), adresse=fake.street_address(), experience=fake.pyint(min_value=1, max_value=5), note=fake.pyint(min_value=1, max_value=10)))
            for e in session1.query(Employe).filter_by(code_postal = r.code_postal,poste = "Manager").all():
                for i in range(0, fake.pyint(min_value=1, max_value=max_employe)):
                    session1.add(Employe(code_postal=r.code_postal, poste=random.choice(["Cassier", "Cuisinier"]), experience=fake.pyint(min_value=1, max_value=5), note=fake.pyint(min_value=1, max_value=10),id_superieur=e.id_employe, nom=fake.last_name(), adresse=fake.street_address()))
    session1.commit()

generateEmploye(5, 10)

def generateRib():
    """
    Fonction qui genere des rib pour chaque employé
    """

    for r in session1.query(Restaurant).all():
        employes = session1.query(Employe).filter_by(code_postal = r.code_postal).all()
        for e in employes:
            session1.add(Rib(id_employe=e.id_employe, iban=fake.unique.iban(), bic=fake.unique.swift(), proprietaire=e.nom))
    
    session1.commit()

generateRib()

def generatePaie():
    """
    Fonction qui genere des paie pour chaque employé
    """
    for pays in session1.query(Pays).all():
        for restaurant in pays.get_all_restaurant():
            restaurant.generate_paie()
    session1.commit()
    
generatePaie()


def generateIngre(nb_ingre: int):
    """
    Fonction qui genere des ingredients dans la BDD
    : param nb_ingredient int : Nombre d'ingredients à générer
    """

    for _ in range(0, nb_ingre):
        rd = random.randint(1,5)
        ingre = Ingredient(nom_ingredient=fake.unique.ingredient(),cout = rd)
        session1.add(ingre)
        
    session1.commit()

generateIngre(100)

def generateItems():
    """
    Fonction qui genere des items par rapport a une liste de boissons,plats, desserts
    """
    
    listBoisson = ["Coca-cola","Fanta","Pepsi","Sprite","Oasis","Ice-Tea","Canada-dry","Perrier","Evian"]
    listPlat = ["Hamburger","Nuggets","Sandwich"]
    listDessert = ["Milk-shake","glace","fruit","crepe","gauffres","Sunday"]
    listTaille = [" S"," M"," L"]
   
    for i in listBoisson:
        for j in listTaille:
            rd = random.randint(1,10)

            items = Item(nom_item = i+j, type = "Boisson",prix = rd)
            session1.add(items)
    
    for i in listPlat:
        rd = random.randint(1,10)

        items = Item(nom_item = i , type = "Plat",prix = rd)
        session1.add(items)

    for i in listDessert:
        rd = random.randint(1,10)

        items = Item(nom_item = i , type = "Dessert",prix = rd)
        session1.add(items)  

    session1.commit() 

generateItems()

def generateRecette():
    """
    Fonction qui genere des recette par rapport a la liste d'ingredients 
    """
    for i in session1.query(Item).all():
        rd = random.randint(100,2500)
        rd2 = random.randint(1,5)
        if i.type == "Plat" or i.type == "Dessert":
            for j in range(rd2):
                recette = Recette(nom_item = i.nom_item ,nom_ingredient = random.choice(session1.query(Ingredient).all()).nom_ingredient, quantite = rd )
                session1.add(recette)
        if i.type == "Boisson" :
            recette = Recette(nom_item = i.nom_item ,nom_ingredient = i.nom_item, quantite = rd )
            session1.add(recette)
    session1.commit()

generateRecette()

def generateStock():
    """
    Fonction qui genere les stocks des ingrédients
    """
    for i in session1.query(Restaurant).all():
        rd = random.randint(200,5000)
        for j in session1.query(Ingredient).all():
            stock = Stock(code_postal = i.code_postal,nom_ingredient= j.nom_ingredient,quantite = rd)
            session1.add(stock)
    session1.commit()

generateStock()


def generateMenu():
    """
    Fonction qui genere les menus
    """
    rd = random.randint(4,10)
    for i in session1.query(Restaurant).all():
        for j in range(rd):
            menu = Menu(boisson =random.choice(session1.query(Item).filter(Item.type == "Boisson").all()).nom_item,
            plat = random.choice(session1.query(Item).filter(Item.type == "Plat").all()).nom_item,
            dessert = random.choice(session1.query(Item).filter(Item.type =="Dessert").all()).nom_item,
            prix = random.randint(5,10))
            session1.add(menu)
            session1.commit()

generateMenu()

def generateCarteItem():
    """
    Fonction qui genere les cartes des items
    """
    for i in session1.query(Pays).all():
        for j in session1.query(Item).all():
             carteItem = CarteItem(pays = i.pays,nom_item = j.nom_item)
             session1.add(carteItem)
             session1.commit()

generateCarteItem()

def generateBill():
    """
    Fonction qui genere les factures
    """
    listMoyPay = ["Carte_bleue","Especes","Cheque","Ticket_restaurant"]
    for i in session1.query(Pays).all():
        for j in session1.query(Restaurant).all():
            bill = Bill(code_postal = j.code_postal,
            id_vendeur = random.choice(session1.query(Employe).all()).id_employe,
            moyen_paiement = random.choice(listMoyPay),
            prix_total = random.randint(8,20) )
            session1.add(bill)
            session1.commit()


generateBill()


def generatePanierItem():
    """
    Fonction qui genere les panier d'items
    """
    for i in session1.query(Restaurant).all():
        for j in session1.query(Bill).all():
            panierItem = PanierItem(nom_item =random.choice(session1.query(Item).all()).nom_item,
            id_bill = j.id_bill,
            quatite = random.randint(5,20))
            session1.add(panierItem)
            session1.commit()

generatePanierItem()

def generatePanierMenu():
    """
    Fonction qui genere les panier d'items
    """
    for i in session1.query(Restaurant).all():
        for j in session1.query(Bill).all():
            panierMenu = PanierMenu(id_bill = j.id_bill,id_menu = session1.query(Menu).all().id_menu,quantité = random.randint(5,20))
            session1.add(panierMenu)
            session1.commit()


generatePanierMenu()

def generateCarteMenu():
    """
    Fonction qui genere les menus de cartes
    """
    for i  in session1.query(Pays).all():
        carteMenu = CarteMenu(pays = i.pays,id_menu = session1.query(Menu).all().id_menu)
        session1.add(carteMenu)
        session1.commit()
    session1.commit()

generateMenu()

from crud import *



session1.close() # On ferme notre session1


