from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, CheckConstraint, ForeignKey, REAL, PrimaryKeyConstraint
import random
from datetime import date, datetime

# Connection à la BDD
engine = create_engine('sqlite:///db.sqlite')
Base = declarative_base()

Session = sessionmaker(bind=engine) # On créer une session qui écoute "Engine"
session = Session()

### Génération des tables & des colonnes avec SQLAlchemy
class Pays(Base):
    __tablename__ = "Pays"

    pays = Column(String, primary_key=True)

    def get_all_restaurant(self):
        """
        Method qui retourne la liste des restaurants du pays
        return list : Liste des restaurants du pays
        """
        return session.query(Restaurant).filter_by(pays = self.pays).all()


class Restaurant(Base):
    __tablename__ = "Restaurant"

    code_postal = Column(String, primary_key=True)
    pays = Column(String, ForeignKey('Pays.pays'))
    capacite = Column(Integer, default=0)
    espace_enfant = Column(SmallInteger, default=0)
    service_rapide = Column(SmallInteger, default=0)
    accessibilite = Column(SmallInteger, default=0)
    parking = Column(SmallInteger, default=0)

    def delete(self):
        """
        Method qui permets de supprimer le restaurant
        """
        session.delete(session.query(Restaurant).filter_by(code_postal = self.code_postal).first()) 
        session.commit()
    
    def update(self, capacite:int, espace_enfant:int, service_rapide:int, accessibilite:int, parking:int):
        """
        Method qui permets de mettre à jour les données du restaurant
        """
        resto = session.query(Restaurant).filter_by(code_postal = self.code_postal)
        resto.update({Restaurant.capacite:capacite, Restaurant.espace_enfant:espace_enfant, Restaurant.service_rapide:service_rapide, Restaurant.accessibilite:accessibilite, Restaurant.parking:parking}, synchronize_session = False)
        session.commit()


    def get_directeur(self):
        """
        Method qui retourne le directeur du restaurant
        return Employe : l'objet du directeur
        """
        return session.query(Employe).filter_by(code_postal = self.code_postal, poste = "Directeur").first()

    def get_all_manager(self):
        """
        Method qui retourne tous les manager du restaurant
        retur list : Liste de manager
        """

        return session.query(Employe).filter_by(code_postal = self.code_postal, poste = "Manager").all()

    def get_all_employe(self):
        """
        Method qui retourne la liste des employés du restaurant
        return list : Liste des employés du restaurant
        """
        return session.query(Employe).filter_by(code_postal = self.code_postal).all()


    def get_employe(self, id_employe):
        """
        Method qui retourne les informations de l'employé du restaurant
        return Employe : Objet de l'employé
        """
        return session.query(Employe).filter(Employe.id_employe == id_employe,Employe.code_postal==self.code_postal)

    def create_employe(self, nom: str, poste: str, adresse: str):
        """
        Method qui créé un nouvel employé au restaurant
        """
        id_superieur = None
        if poste.lower() == "manager":
            id_superieur = self.find_directeur().id_employe
            session.add(Employe(code_postal=self.code_postal, poste="Manager", id_superieur=id_superieur, nom=nom, adresse=adresse))
        elif poste.lower() == "directeur":
            if self.find_directeur() != None:
                return
            else:
                session.add(Employe(code_postal=self.code_postal, poste="Directeur", nom=nom, adresse=adresse))
        else:
            id_superieur = random.choice(self.find_manager()).id_employe
            session.add(Employe(code_postal=self.code_postal, poste=poste, id_superieur=id_superieur, nom=nom, adresse=adresse))
        
        session.commit()
    
    
    def update_employe(self, id_employe: int, new_adress: str):
        """
        Method qui met a jour un employé du restaurant
        """
        employe = self.get_employe(id_employe)
        employe.update({Employe.adresse:new_adress}, synchronize_session = False)
        session.commit()


    def delete_employe(self, id_employe):
        """
        Method qui supprime un employé du restaurant
        """
        session.delete(session.query(Employe).filter_by(code_postal = self.code_postal, id_employe = id_employe).first()) 
        session.commit()

    def generate_paie(self):
        """
        Method qui genere les paies pour chaques employé en fonction de leur role, note, experience
        """
        for employe in self.get_all_employe():
            coeff = ((employe.note / 10) + employe.experience) / 100

            now = datetime.now()
            date = now.strftime("%d/%m/%Y")

            if employe.poste == "Directeur":
                salaire = 3000
                salaire += salaire * coeff
            elif employe.poste == "Manager":
                salaire = 2000
                salaire += salaire * coeff
            else:
                salaire = 1200
                salaire += salaire * coeff
            session.add(Paie(date=date, id_employe=employe.id_employe, salaire_net=salaire))
        
        session.commit()





class Employe(Base):
    __tablename__ = "Employe"

    id_employe = Column(Integer, primary_key=True)
    code_postal = Column(String, ForeignKey('Restaurant.code_postal'))
    id_superieur = Column(Integer, ForeignKey('Employe.id_employe'), nullable=True)
    poste = Column(String)
    experience = Column(Integer, default=0)
    nom = Column(String)
    adresse = Column(String)
    note = Column(Integer, default=5)

    def get_all_paie(self):
        """
        Method qui retourne la liste des salaires de l'employé
        return list : Liste des salaires
        """
        return session.query(Paie).filter_by(id_employe = self.id_employe).all()

    def get_restaurant(self):
        """
        Method qui retourne le restaurant de l'employé
        return Restaurant : Objet du restaurant
        """
        return session.query(Restaurant).filter_by(code_postal = self.code_postal).first()
    
    def get_rib(self):
        """
        Method qui retourne le rib de l'employé
        return Rib : rib de l'employé
        """
        return session.query(Rib).filter_by(id_employe = self.id_employe).first()

class Rib(Base):
    __tablename__ = "Rib"

    id_employe = Column(Integer, ForeignKey('Employe.id_employe'), primary_key=True)
    iban = Column(String)
    bic = Column(String)
    proprietaire = Column(String)

class Paie(Base):
    __tablename__ = "Paie"

    date = Column(String, primary_key=True)
    id_employe = Column(String, ForeignKey('Employe.id_employe'), primary_key=True)
    salaire_net = Column(REAL)

class Item(Base):
    __tablename__ = "Item"

    nom_item = Column(String, primary_key=True)
    type = Column(String)
    prix = Column(REAL)

class Ingredient(Base):
    __tablename__ = "Ingredient"

    nom_ingredient = Column(String, primary_key=True)
    cout = Column(REAL)

class Recette(Base):
    __tablename__ = "Recette"

    nom_item = Column(String, ForeignKey('Item.nom_item'), primary_key=True)
    nom_ingredient = Column(String, ForeignKey('Ingredient.nom_ingredient'), primary_key=True)
    quantite = Column(Integer)

class CarteItem(Base):
    __tablename__ = "CarteItem"

    pays = Column(String, ForeignKey('Pays.pays'), primary_key=True)
    nom_item = Column(String, ForeignKey('Item.nom_item'), primary_key=True)

class Stock(Base):
    __tablename__ = "Stock"

    code_postal = Column(String, ForeignKey('Restaurant.code_postal'), primary_key=True)
    nom_ingredient = Column(String, ForeignKey('Ingredient.nom_ingredient'), primary_key=True)
    quantite = Column(Integer)

class Bill(Base):
    __tablename__ = "Bill"

    id_bill = Column(Integer, primary_key=True)
    code_postal = Column(String, ForeignKey('Restaurant.code_postal'))
    id_vendeur = Column(Integer, ForeignKey('Employe.id_employe'))
    borne = Column(SmallInteger, default=0)
    moyen_paiement = Column(String)
    prix_total = Column(REAL)

class PanierItem(Base):
    __tablename__ = "PanierItem"

    nom_item = Column(String, ForeignKey('Item.nom_item'), primary_key= True)
    id_bill = Column(Integer, ForeignKey('Bill.id_bill'), primary_key=True)
    quatite = Column(Integer)

class Menu(Base):
    __tablename__ = "Menu"

    id_menu = Column(Integer, primary_key=True)
    boisson = Column(String, ForeignKey('Item.nom_item'))
    plat = Column(String, ForeignKey('Item.nom_item'))
    dessert = Column(String, ForeignKey('Item.nom_item'))
    prix = Column(REAL)

class PanierMenu(Base):
    __tablename__ = "PanierMenu"

    id_bill = Column(Integer, ForeignKey('Bill.id_bill'), primary_key=True)
    id_menu = Column(Integer, ForeignKey('Menu.id_menu'), primary_key=True)
    quantite = Column(Integer)

# Enregistrement des tables
Base.metadata.create_all(engine)