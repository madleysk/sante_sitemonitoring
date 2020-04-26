from flask import Flask, render_template, jsonify, request, session, redirect, flash, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from models import *
from forms import *
from auth import *
from authentication import auth
from datetime import datetime
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.register_blueprint(auth)
#app.register_blueprint(site)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_9#y6K"G4Q0c\n\xec]/'
DATABASE_URL='mysql://admin:MyPassw0rd#1@localhost/sante_sm_db' #Mysql database
SQLite_URL = 'sqlite:///database/mydb.db' # Sqlite Database
UPLOAD_PATH='/home/madleysk/sante_sitemonitoring/uploaded/'
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER']=UPLOAD_PATH
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

PER_PAGE= 20

# default page
@app.route('/')
def index():
	page_title = 'Dashboard'
	#db.drop_all()
	#initDb()
	#import_csv_ev("liste_sites.csv",'Site')
	#import_csv_ev("complete_event_list.csv",'Evenement')
	data = {}
	filtre = request.args.get('filter')
	if filtre != None and filtre != 'all':
		data['internet_status'] = {"up":Site.query.filter_by(internet ='up',region=filtre).count(),"down":Site.query.filter_by(internet = 'down').count()}
		data['isante_status'] = {"up":Site.query.filter_by(isante ='up',region=filtre).count(),"down":Site.query.filter_by(isante = 'down').count()}
		data['fingerprint_status'] = {"up":Site.query.filter_by(fingerprint ='up',region=filtre).count(),"down":Site.query.filter_by(fingerprint = 'down').count()}
		data['recent_events'] = Evenement.query.join(Site, Evenement.code_site==Site.code)\
		.filter_by(region=filtre)\
		.add_columns(Evenement.entite_concerne.label('element'),Evenement.status_ev,Evenement.date_rap,Site.nom)\
		.order_by(Evenement.date_rap.desc()).limit(5)
		data['top_bad_sites'] = db.session.query( Evenement.code_site.label('code_site'),func.count(Evenement.code_site).label('qte'), Site.nom.label('nom_site'))\
		.filter_by(status_ev='down')\
		.join(Site, Evenement.code_site==Site.code)\
		.filter_by(region=filtre)\
		.group_by(Evenement.code_site).limit(5)
	else:
		data['internet_status'] = {"up":Site.query.filter_by(internet ='up').count(),"down":Site.query.filter_by(internet = 'down').count()}
		data['isante_status'] = {"up":Site.query.filter_by(isante ='up').count(),"down":Site.query.filter_by(isante = 'down').count()}
		data['fingerprint_status'] = {"up":Site.query.filter_by(fingerprint ='up').count(),"down":Site.query.filter_by(fingerprint = 'down').count()}
		data['recent_events'] = Evenement.query.join(Site, Evenement.code_site==Site.code)\
		.add_columns(Evenement.entite_concerne.label('element'),Evenement.status_ev,Evenement.date_rap,Site.nom)\
		.order_by(Evenement.date_rap.desc()).limit(5)
		data['top_bad_sites'] = db.session.query( Evenement.code_site.label('code_site'),func.count(Evenement.code_site).label('qte'), Site.nom.label('nom_site'))\
		.filter_by(status_ev='down')\
		.join(Site, Evenement.code_site==Site.code)\
		.group_by(Evenement.code_site).limit(5)

	return render_template('dashboard.html', page_title=page_title,data=data,filtre=filtre)


# Site
@app.route('/list_sites', methods=['GET','POST'])
@app.route('/list_sites/page/<int:page>', methods=['GET','POST'])
def list_sites(page=1):
	"""List of sites with pagination enabled"""
	page_title = 'Liste des sites'
	keyword= request.args.get('search')
	if keyword == None:
		liste_sites = Site.query.order_by(Site.nom.asc()).paginate(page,per_page=PER_PAGE)
	else:
		keyword = "%"+keyword+"%"
		liste_sites = Site.query.filter(Site.nom.like(keyword)).paginate(page,per_page=PER_PAGE)

	return render_template("sites_list.html",page_title=page_title,liste_sites=liste_sites)

@app.route('/edit_site/<int:id_site>', methods=['GET','POST'])
def edit_site(id_site):
	page_title = 'Modifier site'
	data= {}
	data['liste_regions']= ['CENTRE','SUD','NORD']
	data['liste_depts']= ['Ouest','Nord','Nord-Est','Nord-Ouest','Sud','Sud-Est','Nippes','Centre','Grand\'Anse']
	site = Site.query.get(id_site)
	
	form = SiteForm(request.form)
	if request.method == 'GET':
		form.code.data= site.code 
		form.type_site.data= site.type_site 
		form.nom.data= site.nom 
		form.sigle.data= site.sigle 
		form.region.data= site.region 
		form.departement.data= site.departement 
		form.commune.data= site.commune 
		form.adresse.data= site.adresse 
		form.pepfar.data= site.pepfar 
		form.contact_1.data= site.contact_1 
		form.tel_1.data= site.tel_1
		form.contact_2.data= site.contact_2 
		form.tel_2.data= site.tel_2
		form.fai.data= site.fai 
		form.internet.data= site.internet 
		form.isante.data= site.isante 
		form.fingerprint.data= site.fingerprint 
	if request.method == 'POST' and form.validate():
		site.code= form.code.data 
		site.type_site= form.type_site.data 
		site.nom= form.nom.data 
		site.sigle= form.sigle.data 
		site.region= form.region.data 
		site.departement= form.departement.data 
		site.commune= form.commune.data 
		site.adresse= form.adresse.data 
		site.pepfar= form.pepfar.data 
		site.contact_1= form.contact_1.data 
		site.tel_1= form.tel_1.data 
		site.contact_2= form.contact_2.data 
		site.tel_2= form.tel_2.data 
		site.fai= form.fai.data 
		site.internet= form.internet.data 
		site.isante= form.isante.data 
		site.fingerprint= form.fingerprint.data
		db.session.commit()
		
		redirect(url_for('site',id_site=id_site))
	return render_template("site_edit.html",page_title=page_title,form=form)

@app.route('/add_site', methods=['GET','POST'])
def add_site():
	page_title = 'Ajouter site'
	data= {}
	data['liste_regions']= ['CENTRE','SUD','NORD']
	data['liste_depts']= ['Ouest','Nord','Nord-Est','Nord-Ouest','Sud','Sud-Est','Nippes','Centre','Grand\'Anse']
	
	form = SiteForm(request.form)
	if request.method == 'POST' and form.validate():
		code= form.code.data 
		type_site= form.type_site.data 
		nom= form.nom.data 
		sigle= form.sigle.data 
		region= form.region.data 
		departement= form.departement.data 
		commune= form.commune.data 
		adresse= form.adresse.data 
		pepfar= form.pepfar.data 
		contact_1= form.contact_1.data 
		tel_1= form.tel_1.data 
		contact_2= form.contact_2.data 
		tel_2= form.tel_2.data 
		fai= form.fai.data 
		internet= form.internet.data 
		isante= form.isante.data 
		fingerprint= form.fingerprint.data
		
		new_site = Site(code,type_site,nom,sigle,region,departement,commune,adresse,pepfar,contact_1,tel_1,contact_2,tel_2,fai,internet,isante,fingerprint)
		db.session.add(new_site)
		db.session.commit()
		flash('Thanks for registering')
	return render_template("site_add.html",page_title=page_title,form=form)

@app.route('/site/<int:id_site>')
@login_required
def site(id_site):
	page_title = 'Information sur le site'
	site = Site.query.get(id_site)
	return render_template("site.html",page_title=page_title,site=site)

# Evenement
@app.route('/add_event',methods=['GET','POST'])
@login_required
def add_event():
	page_title = 'Ajouter un evenement'
	liste_sites = Site.query.all()
	liste_raisons = Source_ev.query.all()

	form = EvenementForm(request.form)
	form.code_site.choices = [('','Selectionner')]+[(s.code,s.nom) for s in Site.query.order_by(Site.nom.asc()).add_columns(Site.code,Site.nom).all() ]
	liste_ev = ['N/A','Probleme FAI','Probleme Interne','Probleme non identifie','Source non identifie']
	form.raison_ev.choices = [('','Selectionner')]+[(v,v) for v in liste_ev]
	form.date_entree.data= datetime.now()
	form.code_utilisateur.data= current_user.code
	if request.method == 'POST' and form.validate():
		code_site= form.code_site.data
		entite_concerne= form.entite_concerne.data
		status_ev= form.status_ev.data
		raison_ev= form.raison_ev.data
		date_ev= form.date_ev.data
		date_rap= form.date_rap.data
		date_entree= datetime.now() # current date and time
		pers_contact= form.pers_contact.data
		remarques= form.remarques.data
		code_utilisateur= form.code_utilisateur.data
		#inserting new event in the database
		new_ev = Evenement(code_site,entite_concerne,status_ev,date_ev,raison_ev,date_rap,pers_contact,remarques,date_entree,code_utilisateur)
		db.session.add(new_ev)
		db.session.commit()
		flash('Operation reussie !')
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
	return render_template("event_new.html",page_title=page_title,form=form)

@app.route('/list_events')
@app.route('/list_events/page/<int:page>')
@login_required
def list_events(page=1):
	page_title = 'Liste evenements'
	keyword = request.args.get('search')
	if keyword == None:
		pagination = Evenement.query.join(Site, Evenement.code_site==Site.code)\
		.add_columns(Evenement.entite_concerne,Evenement.status_ev,Evenement.code_site,Site.nom,Site.fai,Site.departement,Site.region,Evenement.date_ev)\
		.filter(Evenement.code_site==Site.code)\
		.filter(Site.code==Evenement.code_site)\
		.order_by(Evenement.date_rap.desc())\
		.paginate(page,per_page=PER_PAGE)
	else:
		keyword= "%"+keyword+"%"
		pagination = Evenement.query.join(Site, Evenement.code_site==Site.code)\
                .add_columns(Evenement.entite_concerne,Evenement.status_ev,Evenement.code_site,Site.nom,Site.fai,Site.departement,Site.region,Evenement.date_ev)\
                .filter(Evenement.code_site==Site.code)\
                .filter(Site.code==Evenement.code_site)\
		.filter(Site.nom.like(keyword) | Evenement.entite_concerne.like(keyword))\
                .order_by(Evenement.date_rap.desc())\
                .paginate(page,per_page=PER_PAGE)

	return render_template("events_list.html",page_title=page_title,pagination=pagination)

# Employe
@app.route('/list_employes')
@app.route('/list_employes/page/<int:page>')
@login_required
def list_employes(page=1):
	page_title = 'Liste employes'
	keyword= request.args.get('search')
	if keyword == None:
		liste_employes = Employe.query.join(Poste, Employe.poste==Poste.id)\
		.join(Site,Employe.bureau_affecte==Site.code)\
		.add_columns(Employe.nom,Employe.prenom,Poste.nom_poste,Employe.email,Employe.tel_travail,Site.nom.label('bureau_affecte'))\
		.order_by(Employe.nom.asc())\
		.paginate(page,per_page=PER_PAGE)
	else:
		keyword = "%"+keyword+"%"
		liste_employes = Employe.query.join(Poste, Employe.poste==Poste.id)\
		.join(Site,Employe.bureau_affecte==Site.code)\
		.add_columns(Employe.nom,Employe.prenom,Poste.nom_poste,Employe.email,Employe.tel_travail,Site.nom.label('bureau_affecte'))\
		.filter(Employe.nom.like(keyword) | Employe.prenom.like(keyword))\
		.order_by(Employe.nom.asc())\
		.paginate(page,per_page=PER_PAGE)
		
	
	return render_template("employes_list.html",page_title=page_title,liste_employes=liste_employes)

@app.route('/add_employe', methods=['GET','POST'])
@login_required
def add_employe():
	page_title = 'Ajouter employe'
	form = EmployeForm(request.form)
	form.poste.choices = [('','Selectionner')] + [(p.id, p.nom_poste) for p in Poste.query.all()]
	form.bureau_affecte.choices = [('','Selectionner')] +  [(s.code, s.nom) for s in Site.query.order_by(Site.nom.asc()).add_columns(Site.code,Site.nom).all()]
	if request.method == 'POST' and form.validate():
		employe = Employe(code_emp=form.code_emp.data,nom=form.nom.data,prenom=form.prenom.data\
		,email=form.email.data,poste=form.poste.data,adresse=form.adresse.data\
		,tel_perso=form.tel_perso.data,tel_travail=form.tel_travail.data,bureau_affecte=form.bureau_affecte.data)
		flash('Operation completed successfuly !')
	return render_template("employe_add.html",page_title=page_title,form=form)
# User
@app.route('/list_users')
@app.route('/list_users/page/<int:page>')
@login_required
def list_users(page=1):
	page_title = 'Liste Utilisateurs'
	keyword= request.args.get('search')
	if keyword == None:
		liste_users = Users.query.join(Role, Users.auth_level==Role.auth_level)\
		.add_columns(Users.code,Users.username,Users.created_on,Users.modified_on,Role.role_desc.label('role'))\
		.order_by(Users.username.asc()).paginate(page,PER_PAGE)
	else:
		keyword = "%"+keyword+"%"
		liste_users = Users.query.join(Role, Users.auth_level==Role.auth_level)\
		.add_columns(Users.code,Users.username,Users.created_on,Users.modified_on,Role.role_desc.label('role'))\
		.filter(Users.username.like(keyword))\
		.order_by(Users.username.asc()).paginate(page,PER_PAGE)

	return render_template("users_list.html",page_title=page_title,liste_users=liste_users)

@app.route('/add_user', methods=['GET','POST'])
@login_required
def add_user():
	page_title = 'Ajouter utilisateur'
	form = RegistrationForm(request.form)
	form.auth_level.data = 1
	if request.method == 'POST' and form.validate():
		valid_data = True
		username=form.username.data
		passwd= form.passwd.data
		auth_level= form.auth_level.data
		code= form.code.data
		user_exists = Users.query.filter_by(username=username).first()
		code_exists = Users.query.filter_by(code=code).first()
		code_valid = Employe.query.filter_by(code_emp=code).first()
		if code_exists is not None:
			form.code.errors.append('Code not available !')
			valid_data = False
		if code_valid is None:
			form.code.errors.append('Code not valide !')
			valid_data = False
		if user_exists is not None:
			form.username.errors.append('Username not available !')
			valid_data = False
		if valid_data == True:
			user = Users(username=username,passwd=pass_hashing(passwd),auth_level=auth_level,code=code)
			db.session.add(user)
			db.session.commit()
		flash('User addedd successfuly')
		
	return render_template('user_add.html',page_title=page_title,form=form)

@app.route('/file_import', methods=['GET','POST'])
@login_required
def file_import():
	page_title = 'Importer'
	ALLOWED_EXTENTIONS={'csv'}
	ALLOWED_FTYPE =['Site','Users','Employe','Evenement']
	type_fichier = request.args.get('ftype')
	form = FileImportForm(request.form)
	form.type_fichier.data=type_fichier
	warning=''
	infos={}
	infos['Site']= "\
	code,type_site,nom,sigle,region,departement,commune,adresse,\
	pepfar,contact_1,tel_1,contact_2,tel_2,fai,internet,isante,fingerprint"
	infos['Users']=''
	infos['Employe']=''
	infos['Evenement']=''
	if type_fichier:
		page_title = 'Importer Liste '+type_fichier+'s'
		if type_fichier in ALLOWED_FTYPE:
			warning=infos[type_fichier]
	if request.method == 'POST':
		file_name = secure_filename(request.files['fichier'].filename)
		type_fichier=request.form.get('type_fichier')
		if file_name != '' and type_fichier !='':
			fichier= request.files['fichier']
			fichier.save(open(os.path.join(UPLOAD_PATH, fichier.filename),'w+b'))
			print(type_fichier)
			import_csv_ev(UPLOAD_PATH+file_name,type_fichier)
			next_page = request.args.get('next')
			return redirect(next_page or url_for('index'))
		else:
			flash('Fichier obligatoire')
		
	return render_template('file_import.html',page_title=page_title,form=form,warning=warning)
	
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

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return Users.query.get(user_id)
    return None
    
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))


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
				date_entree= datetime.now()
				code_utilisateur= current_user.code
				#date_ev=evenement[4]
				#date_rap=evenement[6]
				db.session.add(Evenement(code_site=evenement[0],entite_concerne=evenement[2].lower(),status_ev=evenement[3].lower(),date_ev=evenement[4],raison_ev=evenement[5],date_rap=evenement[6],pers_contact=evenement[7],remarques=evenement[8],date_entree=date_entree,code_utilisateur=code_utilisateur))
			db.session.commit()
		if nom_classe == 'Site':
			for site in lignes_contenu:
				print(len(site))
				db.session.add(Site(code=site[0],type_site=site[1],nom=site[2],sigle='',region=site[3],departement=site[4],commune=site[5],adresse='',pepfar=site[6],contact_1=site[7],tel_1=site[8],contact_2=site[9],tel_2=site[10],fai=site[11],internet=site[12],isante=site[13],fingerprint=site[14]))
			db.session.commit()
		if nom_classe == 'Bureau':
			for bureau in lignes_contenu:
				db.session.add(Bureau(code=bureau[0],pers_resp=bureau[1],fai=bureau[2],adresse=bureau[3],region=bureau[4],departement=bureau[5],tel=bureau[6]))
				db.session.commit()
		if nom_classe == 'Employe':
			for employe in lignes_contenu:
				db.session.add(Employe(code=employe[0],nom=employe[1],prenom=employe[2],email=employe[3],poste=employe[4],adresse=employe[5],tel_perso=employe[6],tel_travail=employe[7],bureau_affecte=employe
				[8]))
			db.session.commit()

if __name__ == '__main__':
	app.run(debug = True)
