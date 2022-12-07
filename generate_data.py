"""
Ce fichier sert à générer des informations fictives avec le module "Faker"
Il nous permets de générer des lignes SQL en fonction des besoins de projet
"""

from conf import * # On importe notre configuration de Table
from faker import Faker
import random

fake = Faker("FR") # On utilise les formats FR de faker pour générer les données
fake.seed_instance(0) # On définis une seed pour que l'aléatoire soit figé durant nos tests



Session = sessionmaker(bind=engine) # On créer une session qui écoute "Engine"
session = Session()

def generateCountry(nb_country: int):
    """
    Fonction qui genere des pays dans la BDD
    : param nb_country int : Nombre de pays à générer
    """
    for _ in range(0, nb_country):
        pays = Pays(pays=fake.unique.country())
        session.add(pays)

    session.commit()

generateCountry(225)

def generateRestaurant(nb_restaurant):
    """
    Fonction qui genere des restaurants dans la BDD
    : param nb_country int : Nombre de pays à générer
    """

    for _ in range(0, nb_restaurant):

        my_country = random.choice(session.query(Pays).all()).pays

        resto = Restaurant(code_postal=fake.unique.postcode(), pays=my_country, capacite=fake.pyint(min_value=10, max_value=200), espace_enfant=fake.pyint(min_value=0, max_value=1), service_rapide=fake.pyint(min_value=0, max_value=1), accessibilite=fake.pyint(min_value=0, max_value=1), parking=fake.pyint(min_value=0, max_value=1))
        session.add(resto)
        
    session.commit()

generateRestaurant(100)

def generateEmploye(max_manager: int, max_employe: int):
    """
    Fonction qui genere les employés de chaques Restaurant
    """

    for r in session.query(Restaurant).all():
        session.add(Employe(code_postal=r.code_postal, poste="Directeur", nom=fake.last_name(), adresse=fake.street_address()))
        for _ in range(0, fake.pyint(min_value=1, max_value=max_manager)):
            session.add(Employe(code_postal=r.code_postal, poste="Manager", id_superieur=session.query(Employe).filter_by(code_postal = r.code_postal).first().id_employe, nom=fake.last_name(), adresse=fake.street_address()))
            for e in session.query(Employe).filter_by(code_postal = r.code_postal, poste = "Manager").all():
                for i in range(0, fake.pyint(min_value=1, max_value=max_employe)):
                    session.add(Employe(code_postal=r.code_postal, poste=random.choice(["Cassier", "Cuisinier"]), id_superieur=e.id_employe, nom=fake.last_name(), adresse=fake.street_address()))
    session.commit()

generateEmploye(5, 10)

def generateRib():
    """
    Fonction qui genere des rib pour chaque employé
    """

    for r in session.query(Restaurant).all():
        employes = session.query(Employe).filter_by(code_postal = r.code_postal).all()
        for e in employes:
            session.add(Rib(id_employe=e.id_employe, iban=fake.unique.iban(), bic=fake.unique.swift(), proprietaire=e.nom))
    
    session.commit()

generateRib()

def generatePaie(nb_paie_max):
    """
    Fonction qui genere des paie pour chaque employé
    """

    for e in session.query(Employe).all():
        for _ in range(0, fake.pyint(min_value=1, max_value=nb_paie_max)):
            if e.poste == "Directeur":
                session.add(Paie(date=fake.unique.date(), id_employe=e.id_employe, salaire_net = fake.pyfloat(right_digits=2, positive=True, min_value=2000.0, max_value=3500.0)))
            elif e.poste == "Manager":
                session.add(Paie(date=fake.unique.date(), id_employe=e.id_employe, salaire_net = fake.pyfloat(right_digits=2, positive=True, min_value=1500.0, max_value=2000.0)))
            else:
                session.add(Paie(date=fake.unique.date(), id_employe=e.id_employe, salaire_net = fake.pyfloat(right_digits=2, positive=True, min_value=900.0, max_value=1800.0)))
    session.commit()

generatePaie(1)






session.close() # On ferme notre session


