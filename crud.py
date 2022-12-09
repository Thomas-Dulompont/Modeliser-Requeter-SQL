from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, CheckConstraint, ForeignKey, REAL, PrimaryKeyConstraint
import random
from datetime import date, datetime
from conf import *

Session1 = sessionmaker(bind=engine1)
session1 = Session1()

engine2 = create_engine('sqlite:///exercices.sqlite')
Session2 = sessionmaker(bind=engine2)
session2 = Session2()

Base = declarative_base()

class Exercice1(Base):
    __tablename__ = "Exercice1"

    date_extract = Column(String)
    departement = Column(String, primary_key=True)
    nb_employe = Column(Integer)

class Exercice3(Base):
    __tablename__ = "Exercice3"

    date_extract = Column(String)
    pays = Column(String, primary_key=True)
    nb_employe = Column(Integer)
    salaire_total = Column(REAL)

Base.metadata.create_all(engine2)

def get_date():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M")
    return date

def exercice1():
    for i in session1.query(Restaurant).group_by(Restaurant.departement).all():
        session2.add(Exercice1(date_extract=get_date(),departement=i.departement, nb_employe=len(i.get_all_employe())))
        
    session2.commit()

exercice1()

def exercice3():
    for pays in session1.query(Pays).all():
        nb_employe = 0
        salaire_total = 0
        for restaurant in pays.get_all_restaurant():
            nb_employe += len(restaurant.get_all_employe())
            for employe in restaurant.get_all_employe():
                for salaire in employe.get_all_paie():
                    salaire_total += salaire.salaire_net
        salaire_total = round(salaire_total, 3)
        session2.add(Exercice3(date_extract=get_date(), pays=pays.pays, nb_employe=nb_employe, salaire_total=salaire_total))
    session2.commit()

exercice3()