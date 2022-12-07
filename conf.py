from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, CheckConstraint, ForeignKey, REAL, PrimaryKeyConstraint

# Connection à la BDD
engine = create_engine('sqlite:///db.sqlite')
Base = declarative_base()

### Génération des tables & des colonnes avec SQLAlchemy
class Pays(Base):
    __tablename__ = "Pays"

    pays = Column(String, primary_key=True)

class Restaurant(Base):
    __tablename__ = "Restaurant"

    code_postal = Column(String, primary_key=True)
    pays = Column(String, ForeignKey('Pays.pays'))
    capacite = Column(Integer, default=0)
    espace_enfant = Column(SmallInteger, default=0)
    service_rapide = Column(SmallInteger, default=0)
    accessibilite = Column(SmallInteger, default=0)
    parking = Column(SmallInteger, default=0)

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