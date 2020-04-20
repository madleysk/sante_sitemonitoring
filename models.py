import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from auth import *
from datetime import datetime


db = SQLAlchemy()

class Bureau(db.Model):
	__tablename__ = "bureaux"
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(10),unique=True,nullable=False)
	pers_resp = db.Column(db.String(160),nullable=False)
	fai = db.Column(db.String(20))
	adresse = db.Column(db.String(160))
	region = db.Column(db.String(20),nullable=False)
	departement = db.Column(db.String(30),nullable=False)
	tel = db.Column(db.String(15))
	employes = db.relationship("Employe", backref="bureau_emp", lazy=True)
	sites = db.relationship("Site", backref="bureau_site", lazy=True)
    
	def __init__(self,code,pers_resp,fai,adresse,region,departement,tel):
		self.code=code
		self.pers_resp=pers_resp
		self.fai=fai
		self.adresse=adresse
		self.region=region
		self.departement=departement
		self.tel=tel
		
	def ajouter_employe(self,code,nom,prenom,email,poste,adresse,tel_perso,tel_travail):
		new_employe = Employe(code,nom,prenom,email,poste,adresse,tel_perso,tel_travail,self.code)
		db.session.add(new_employe)
		db.session.commit()
		
	def ajouter_site(self,code,nom,sigle,pers_resp,fai,adresse,region,departement,tel,internet,isante,fingerprint):
		new_site = Site(code,nom,sigle,pers_resp,self.code,fai,adresse,region,departement,tel,internet,isante,fingerprint)
		db.session.add(new_site)
		db.session.commit()


class Site(db.Model):
	__tablename__ = "sites"
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(10),unique=True,nullable=False)
	nom = db.Column(db.String(100),unique=True,nullable=False)
	sigle = db.Column(db.String(20),unique=True,nullable=False)
	pers_resp = db.Column(db.String(100),nullable=False)
	bureau_resp = db.Column(db.String(10), db.ForeignKey("bureaux.code"))
	fai = db.Column(db.String(20))
	adresse = db.Column(db.String(160))
	region = db.Column(db.String(20),nullable=False)
	departement = db.Column(db.String(30),nullable=False)
	tel = db.Column(db.String(15))
	internet = db.Column(db.String(5))
	isante = db.Column(db.String(5))
	fingerprint = db.Column(db.String(5))
    
	def __init__(self,code,nom,sigle,pers_resp,bureau_resp,fai,adresse,region,departement,tel,internet,isante,fingerprint):
		self.code=code
		self.nom=nom
		self.sigle=sigle
		self.pers_resp=pers_resp
		self.bureau_resp=bureau_resp
		self.fai=fai
		self.adresse=adresse
		self.region=region
		self.departement=departement
		self.tel=tel
		self.internet=internet
		self.isante=isante
		self.fingerprint=fingerprint
		

class Poste(db.Model):
	__tablename__ = "postes"
	id = db.Column(db.Integer, primary_key=True)
	nom_poste = db.Column(db.String(100))
	categorie_poste = db.Column(db.String(10))
	domaine_poste = db.Column(db.String(50))
	dept = db.Column(db.String(50))
	
	def __init__(self,nom_poste,categorie_poste,domaine_poste,dept):
		self.nom_poste = nom_poste
		self.categorie_poste = categorie_poste
		self.domaine_poste = domaine_poste
		self.dept = dept

class Employe(db.Model):
	__tablename__ = "employes"
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(10),unique=True,nullable=False)
	nom = db.Column(db.String(160))
	prenom = db.Column(db.String(160))
	email = db.Column(db.String(200),unique=True,nullable=False)
	poste = db.Column(db.Integer,db.ForeignKey("postes.id"),nullable=False)
	adresse = db.Column(db.String(160))
	tel_perso = db.Column(db.String(15))
	tel_travail = db.Column(db.String(15))
	bureau_affecte = db.Column(db.String(10), db.ForeignKey("bureaux.code"))

	def __init__(self,code,nom,prenom,email,poste,adresse,tel_perso,tel_travail,bureau_affecte):
		self.code=code
		self.nom = nom
		self.prenom = prenom
		self.email = email
		self.poste = poste
		self.adresse = adresse
		self.tel_perso = tel_perso
		self.tel_travail = tel_travail
		self.bureau_affecte = bureau_affecte

class Role(db.Model):
	__tablename__ = "roles"
	id = db.Column(db.Integer, primary_key=True)
	auth_level = db.Column(db.Integer,unique=True,nullable=False)
	role_desc = db.Column(db.String(50),nullable=False) 

	def __init__(self,auth_level,role_desc):
		self.auth_level = auth_level
		self.role_desc = role_desc

class Users(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(40),unique=True,nullable = False)
	passwd = db.Column(db.String(256),nullable = False)
	auth_level = db.Column(db.Integer,db.ForeignKey("roles.auth_level"),nullable = False)
	code = db.Column(db.String(10),db.ForeignKey("employes.code"),nullable= False)

	def __init__(self,username,passwd,auth_level,code):
		self.username = username
		self.passwd = passwd
		self.auth_level = auth_level
		self.code = code

class Source_ev(db.Model):
	__tablename__ = "source_ev"
	id = db.Column(db.Integer, primary_key=True)
	desc_ev = db.Column(db.String(100),nullable=False)
	
	def __init__(self,desc_ev):
		self.desc_ev=desc_ev
		
		
class Evenement(db.Model):
	__tablename__ = "evenements"
	id = db.Column(db.Integer, primary_key=True)
	code_site = db.Column(db.String(10),db.ForeignKey("sites.code"),nullable=False)
	entite_concerne = db.Column(db.String(15),nullable = False) # internet, isante or fingerprint
	status_ev = db.Column(db.String(10),nullable = False) # up, down, none
	src_ev = db.Column(db.Integer,db.ForeignKey("source_ev.id"),nullable = False)
	date_ev = db.Column(db.DateTime,nullable = False)
	date_rap = db.Column(db.DateTime,nullable = False)
	date_entree = db.Column(db.DateTime,nullable = False, default=datetime.utcnow)
	pers_contact = db.Column(db.String(100),nullable = False)
	remarques = db.Column(db.String(100),nullable = False)
	code_utilisateur = db.Column(db.String(10),db.ForeignKey("users.code"),nullable = False)

	def __init__(self,code_site,entite_concerne,status_ev,src_ev,date_ev,date_rap,date_entree,pers_contact,remarques,code_utilisateur):
		self.code_site=code_site
		self.entite_concerne=entite_concerne
		self.status_ev=status_ev
		self.src_ev=src_ev
		self.date_ev=date_ev
		self.date_rap=date_rap
		self.date_entree=date_entree
		self.pers_contact=pers_contact
		self.remarques=remarques
		self.code_utilisateur=code_utilisateur

def initDb():
	"""Database initializer"""
	db.create_all()
	# Initializing tables database
	# table Source_ev
	liste_ev = ['N/A','Probleme FAI','Probleme Interne','Probleme non identifie','Source non identifie']
	for prob in liste_ev:
		db.session.add(Source_ev(prob))
		db.session.commit()
	# Table roles
	roles =  {}
	roles['01']='user'
	roles['02']='superuser'
	roles['03']='manager'
	roles['09']='admin'
	for  v,k in roles.items():
		db.session.add(Role(int(v),k))
	db.session.commit() # validate insert cause foreign key dependencies
	# Table Postes
	liste_poste= [{"nom_poste":"Manager","categorie_poste":"C4","domaine_poste":"Gestion et Administration","dept":"RH"}]
	liste_poste.append({"nom_poste":"IT Manager","categorie_poste":"C3","domaine_poste":"Computers","dept":"Information & technology"})
	liste_poste.append({"nom_poste":"IT Assistant","categorie_poste":"C2","domaine_poste":"Computers","dept":"Information & technology"})
	for poste in liste_poste:
		db.session.add(Poste(poste['nom_poste'],poste['categorie_poste'],poste['domaine_poste'],poste['dept']))
	db.session.commit()
	# Table Bureaux
	bureau1 = Bureau('PAP-OF01','Nathaniel Segaren','Natcom','Turgeau','Centre','Ouest','5090')
	db.session.add(bureau1)
	db.session.commit()
	# Table Sites
	site1 = Site('H-01','Hopital Communaute Haitienne','HCH','Jean Mackenson Louis','PAP-OF01','Digicel','Route de Freres','Centre','Ouest','50901','up','up','up')
	db.session.add(site1)
	db.session.commit()
	# Table employes
	employe = Employe('1001','Meite','Madley Sk.','madley.meite@carisfoundationintl.org','03','Cayes','509000','50900','PAP-OF01')
	db.session.add(employe)
	db.session.commit()
	# Table users
	admin_user = Users('admin',pass_hashing('Pass0321'),9,'1001')
	db.session.add(admin_user)
	db.session.commit()
