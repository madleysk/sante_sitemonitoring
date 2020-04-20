from flask import Flask, render_template, jsonify, request, session, redirect
from models import *
from auth import *
from datetime import datetime
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_9#y6K"G4Q0c\n\xec]/'
DATABASE_URL='mysql://admin:MyPassw0rd#1@localhost/sante_sm_db' #Mysql database
SQLite_URL = 'sqlite:///database/mydb.db' # Sqlite Database
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route('/',methods=['GET'])
def index():
	page_title = 'Dashboard'
	#db.drop_all()
	#initDb()
	filtering = request.args.get('filter')
	data = {}
	data['internet_status'] = {"up":Site.query.filter_by(internet ='up').count(),"down":Site.query.filter_by(internet = 'down').count()}
	data['isante_status'] = {"up":Site.query.filter_by(isante ='up').count(),"down":Site.query.filter_by(isante = 'down').count()}
	data['fingerprint_status'] = {"up":Site.query.filter_by(fingerprint ='up').count(),"down":Site.query.filter_by(fingerprint = 'down').count()}
	top_bad_sites = db.engine.execute('SELECT code_site, count(*) as qte from evenements WHERE status_ev="down" group by code_site order by qte DESC Limit 5;')
	list_bad =[]
	for site in top_bad_sites:
		list_bad.append(Site.query.filter_by(code=site.code_site).first())
	#data['recent_events']= Evenement.query.order_by(Evenement.date_entree.desc()).limit(5)
	data['recent_events']= db.engine.execute('SELECT entite_concerne as element, status_ev,nom as nom_site,date_entree FROM evenements, sites WHERE evenements.code_site=sites.code ORDER BY date_entree DESC LIMIT 5')
	data['top_bad_sites']= list_bad
	#import_csv_ev("bureaux.csv",'Bureau')
	#import_csv_ev("sites.csv",'Site')
	#import_csv_ev("evenements.csv",'Evenement')
	return render_template('dashboard.html', page_title=page_title,filtering=filtering,data=data)

@app.route('/subscribe')
def subscribe():
	page_title = 'Inscription'
	return render_template('layout.html',page_title=page_title)

@app.route('/login', methods=['GET', 'POST'])
def login():
	page_title = 'Login'
	if request.method == 'POST':
		username = request.form.get('pseudo')
		res = Users.query.filter_by(username=username).first()
		if res != None:
			if(res.username == username):
				passwd = request.form.get('passwd')
				if(pass_verify(passwd,res.passwd)):
					session['username'] = username
					session['auth_level'] = res.auth_level
					session['ucode'] = res.code
					return redirect('/')
				else:
					return render_template("login.html",page_title=page_title,errPWD='Password incorrect')
		else:
			return render_template("login.html",page_title=page_title, errUSR="Username does not exist !")
	return render_template("login.html",page_title = 'Login')

@app.route('/logout')
def logout():
	page_title = 'Dashboard'
	session.clear()
	session['username']=None
	session['auth_level']=None

	return redirect('/')

@app.route('/list_sites')
def list_sites():
	page_title = 'Liste des sites'
	liste_sites = Site.query.all()
	return render_template("liste_sites.html",page_title=page_title,liste_sites=liste_sites)

@app.route('/add_site', methods=['GET','POST'])
def add_site():
	page_title = 'Ajouter site'
	data= {}
	data['liste_bureaux']= Bureau.query.all()
	data['liste_regions']= ['Centre','Sud','Nord']
	data['liste_depts']= ['Ouest','Nord','Nord-Est','Nord-Ouest','Sud','Sud-Est','Nippes','Centre','Grand\'Anse']
	
	if request.method == 'POST':
		code= request.form.get('code')
		nom= request.form.get('nom')
		sigle= request.form.get('sigle')
		pers_resp= request.form.get('pers_resp')
		bureau_resp= request.form.get('bureau_resp')
		fai= request.form.get('fai')
		adresse= request.form.get('adresse')
		region= request.form.get('region')
		departement= request.form.get('departement')
		tel= request.form.get('tel')
		internet= request.form.get('internet')
		isante= request.form.get('isante')
		fingerprint= request.form.get('fingerprint')
		
		new_site = Site(code,nom,sigle,pers_resp,bureau_resp,fai,adresse,region,departement,tel,internet,isante,fingerprint)
		db.session.add(new_site)
		db.session.commit()
	
	return render_template("add_site.html",page_title=page_title,data=data)

@app.route('/site/<int:id_site>')
def site(id_site):
	page_title = 'Information sur le site'
	return render_template("site.html",page_title=page_title)

@app.route('/add_event',methods=['GET','POST'])
def add_event():
	page_title = 'Ajouter un evenement'
	liste_sites = Site.query.all()
	liste_raisons = Source_ev.query.all()
	if request.method == 'POST':
		code_site= request.form.get('code_site')
		entite_concerne= request.form.get('entite_concerne')
		status_ev= request.form.get('status_ev')
		src_ev= request.form.get('src_ev')
		date_ev= request.form.get('date_ev')
		date_rap= request.form.get('date_rap')
		date_entree= datetime.now() # current date and time
		pers_contact= request.form.get('pers_contact')
		remarques= request.form.get('remarques')
		code_utilisateur= session['ucode']
		#inserting new event in the database
		new_ev = Evenement(code_site,entite_concerne,status_ev,src_ev,date_ev,date_rap,date_entree,pers_contact,remarques,code_utilisateur)
		db.session.add(new_ev)
		db.session.commit()
		# updating site infos
		site = Site.query.filter_by(code=code_site).first()
		if entite_concerne == 'internet':
			site.internet = status_ev
			db.session.commit()
		elif entite_concerne == 'isante':
			site.isante = status_ev
			db.session.commit()
		elif entite_concerne == 'fingerprint':
			site.fingerprint = status_ev
			db.session.commit()
		
	return render_template("add_event.html",page_title=page_title,liste_sites=liste_sites,liste_raisons=liste_raisons)

@app.route('/list_events')
def list_events():
	page_title = 'Liste evenements'
	#liste_events= Evenement.query.order_by(Evenement.date_entree.desc()).limit(25)
	liste_events = Evenement.query.order_by(Evenement.date_entree.desc()).paginate(per_page=25).items
	pagination = Evenement.query.order_by(Evenement.date_entree.desc()).paginate(per_page=25)
	return render_template("list_events.html",page_title=page_title,liste_events=liste_events,pagination=pagination)

@app.route('/list_employes')
def list_employes():
	page_title = 'Liste employes'
	return render_template("list_employes.html",page_title=page_title)

@app.route('/add_employe')
def add_employe():
	page_title = 'Ajouter employe'
	return render_template("add_employe.html",page_title=page_title)

@app.route('/list_users')
def list_users():
	page_title = 'Liste Utilisateurs'
	return render_template("list_users.html",page_title=page_title)

@app.route('/import_event',methods=['GET','POST'])
def import_event():
	import_csv_ev("evenements.csv",'Evenement')
	return render_template("add_event.html",page_title=page_title)

@app.route('/add_user')
def add_user():
	page_title = 'Ajouter utilisateur'
	return render_template("add_user.html",page_title=page_title)
	
@app.route('/api/<string:url>', methods=['GET'])
def api(url):
	param = request.args.get('status')
	if url == 'internet':
		return str(Site.query.filter_by(internet = param).count())
	if url == 'isante':
		return str(Site.query.filter_by(isante = param).count())
	if url == 'fingerprint':
		return str(Site.query.filter_by(fingerprint = param).count())
	return jsonify({"error":'An error has occured ! Could not find api params !'})

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
				db.session.add(Bureau(code=bureau[0],pers_resp=bureau[1],fai=bureau[2],adresse=bureau[3],region=bureau[4],departement=bureau[5],tel=bureau[6]))
				db.session.commit()
		if nom_classe == 'Employe':
			for employe in lignes_contenu:
				db.session.add(Employe(code=employe[0],nom=employe[1],prenom=employe[2],email=employe[3],poste=employe[4],adresse=employe[5],tel_perso=employe[6],tel_travail=employe[7],bureau_affecte=employe[8]))
				db.session.commit()

if __name__ == '__main__':
	app.run(debug = True)
