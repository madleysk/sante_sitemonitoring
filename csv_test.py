#!/usr/bin/python3
import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#engine = create_engine('mysql://admin:MyPassw0rd#1@localhost/sante_sm_db')
#db = scoped_session(sessionmaker(bind=engine))

print("Let's import CSV file")

nom_classe = 'Evenement'
with open("evenements.csv") as csv_file:
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
			date_entree= evenement[6]
			pers_contact= evenement[7]
			remarques= evenement[8]
			code_utilisateur= evenement[9]
			print(code_site,entite_concerne,status_ev,src_ev,date_ev,date_rap,date_entree,pers_contact,remarques,code_utilisateur)
