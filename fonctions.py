from flask import session
import csv
from datetime import datetime

def import_csv_ev(fichier,nom_classe):
	with open(fichier) as csv_file:
		csv_reader = csv.reader(csv_file,delimiter=',')
		line_count = 0
		lignes_contenu=[]
		for row in csv_reader:
			if line_count == 0:
				header=", ".join(row).split(",")
				line_count += 1
			else:
				lignes_contenu.append(",".join(row).split(","))
				line_count += 1
		# importing csv file
		if nom_classe == 'Evenement':
			for evenement in lignes_contenu:
				code_site= evenement[0]
				entite_concerne= evenement[1]
				status_ev= evenement[2]
				src_ev= evenement[3]
				date_ev= evenement[4]
				date_rap= evenement[5]
				date_entree= datetime.now()
				pers_contact= evenement[7]
				remarques= evenement[8]
				code_utilisateur= session['ucode']
				print(code_site,entite_concerne,status_ev,src_ev,date_ev,date_rap,date_entree,pers_contact,remarques,code_utilisateur)
				db.session.add(Evenement(code_site,entite_concerne,status_ev,src_ev,date_ev,date_rap,date_entree,pers_contact,remarques,code_utilisateur))
				db.session.commit()
		if nom_classe == 'Site':
			for site in lignes_contenu:
				code= site[0]
				nom= site[1]
				sigle= site[2]
				pers_resp= site[3]
				bureau_resp= site[4]
				fai= site[5]
				adresse= site[6]
				region= site[7]
				departement= site[8]
				tel= site[9]
				internet= site[10]
				isante= site[11]
				fingerprint= site[12]
				db.session.add(Site(code,nom,sigle,pers_resp,bureau_resp,fai,adresse,region,departement,tel,internet,isante,fingerprint))
				db.session.commit()
		if nom_classe == 'Bureau':
			for bureau in lignes_contenu:
				db.session.add(Bureau(code=bureau[0],nom=bureau[1],pers_resp=bureau[2],fai=bureau[3],adresse=bureau[4],region=bureau[5],departement=bureau[6],tel=bureau[7]))
				db.session.commit()
		if nom_classe == 'Employe':
			for employe in lignes_contenu:
				db.session.add(Employe(code=employe[0],nom=employe[1],prenom=employe[2],email=employe[3],poste=employe[4],adresse=employe[5],tel_perso=employe[6],tel_travail=employe[7],bureau_affecte=employe[8]))
				db.session.commit()
