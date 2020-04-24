from wtforms import Form, BooleanField, StringField, PasswordField, SelectField, HiddenField, validators
from wtforms.fields.html5 import DateField, TelField, EmailField

class RegistrationForm(Form):
	username = StringField('Username',[validators.Length(min=4,max=30)])
	passwd = PasswordField('Password',[validators.DataRequired(),validators.EqualTo('pwd_confirm', message='Passwords must match')])
	pwd_confirm = PasswordField('Confirm Password')
	auth_level = StringField('Role',[validators.Length(min=4,max=30)])
	code = StringField('Code',[validators.Length(min=2,max=10,message='Code invalide')])

class SiteForm(Form):
	code= StringField('Code site',[validators.Length(min=2,max=10)])
	type_site= SelectField(u'Type',choices=[('site','Site'),('bureau','Bureau')])
	nom= StringField('Titre Site',[validators.Length(min=4,max=30)])
	sigle= StringField('Sigle')
	region= SelectField(u'Region',choices=[('CENTRE','Centre'),('SUD','Sud'),('NORD','Nord')])
	departement= SelectField(u'Departement',choices=[('ouest','Ouest'),('sud','Sud'),('centre','Centre'),('sud-est','Sud-Est'),('nippes','Nippes')])
	commune= StringField('Commune',[validators.Length(min=4,max=30)])
	adresse= StringField('Adresse',[validators.Length(min=4,max=30)])
	pepfar= SelectField('Site PEPFAR ?',choices=[('oui','Oui'),('Non','Non')])
	contact_1= StringField('Contact 1',[validators.Length(min=4,max=30)])
	tel_1= TelField('Telephone',[validators.Length(min=8,max=15)])
	contact_2= StringField('Contact 2',[validators.Length(min=4,max=30)])
	tel_2= TelField('Telephone',[validators.Length(min=8,max=15)])
	fai= SelectField(u'FAI',choices=[('digicel','Digicel'),('natcom','Natcom'),('access','Access Haiti'),('hainet','Hainet')])
	internet= SelectField(u'Internet Status',choices=[('up','Up'),('down','Down'),('aucun','Aucune Connection')])
	isante= SelectField(u'iSante Status',choices=[('up','Up'),('down','Down'),('aucun','Pas de Serveur')])
	fingerprint= SelectField(u'Fingerprint Status',choices=[('up','Up'),('down','Down'),('aucun','Pas de Serveur')])

class EmployeForm(Form):
	code_emp= StringField('Bureau',[validators.Length(min=2,max=10)])
	nom= StringField('Nom',[validators.Length(min=2,max=60)])
	prenom= StringField('Prenom',[validators.Length(min=2,max=60)])
	email= EmailField('Adresse Email',[validators.Length(min=2,max=60)])
	poste= SelectField('Poste',validate_choice=False)
	adresse= StringField('Adresse Postale',[validators.Length(min=2,max=60)])
	tel_perso= TelField('Telephone Perso',[validators.Length(min=8,max=15)])
	tel_travail= TelField('Telephone Travail',[validators.Length(min=8,max=15)])
	bureau_affecte= SelectField('Bureau Affectation',validate_choice=False)
	
class EvenementForm(Form):
	code_site= SelectField('Site',[validators.DataRequired()])
	entite_concerne= SelectField('Element',[validators.DataRequired()],choices=[('','Selectionner'),('internet','Internet'),('isante','iSante Servveur'),('fingerprint','Fingerprint Servveur')])
	status_ev= SelectField(u'Status',[validators.DataRequired()],choices=[('','Selectionner'),('up','Up'),('down','Down'),('aucun','Pas de Serveur')])
	date_ev= DateField('Date Evenement')
	raison_ev= SelectField('Raison',[validators.DataRequired()])
	date_rap= DateField('Date Rapportage')
	pers_contact= StringField('Personne contactee')
	remarques= StringField('Remarques')
	date_entree= HiddenField('')
	code_utilisateur= HiddenField('')
