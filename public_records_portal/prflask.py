from public_records_portal import app, models, db, views
from views import * # Import all the functions that render templates
from flask.ext.restless import APIManager
from flask.ext.admin import Admin, expose, BaseView, AdminIndexView
from flask.ext.admin.contrib.sqlamodel import ModelView

# Create API
manager = APIManager(app, flask_sqlalchemy_db=db)
# The endpoints created are /api/object, e.g. publicrecordsareawesome.com/api/request/
request_methods = ['contact_name', 'solid_status']
manager.create_api(models.Request,
                   methods=['GET'],
                   results_per_page = 15,
                   max_results_per_page = 100,
                   allow_functions = True,
                   include_methods = request_methods)
manager.create_api(models.Owner, methods=['GET'], results_per_page = 10, allow_functions = True)
manager.create_api(models.Note, methods=['GET'], results_per_page = 10, allow_functions = True)
manager.create_api(models.Record, methods=['GET'], results_per_page = 10, allow_functions = True)
manager.create_api(models.QA, methods=['GET'], results_per_page =10, allow_functions = True)
manager.create_api(models.Subscriber, methods=['GET'], results_per_page = 10, allow_functions = True)
manager.create_api(models.Visualization, methods=['GET'], results_per_page = 10, allow_functions = True)


class HomeView(AdminIndexView):
    @expose('/')
    def home(self):
        return self.render('admin.html')
    def is_accessible(self):
		if current_user.is_authenticated():
			admins = app.config['LIST_OF_ADMINS'].split(",")
			if current_user.email.lower() in admins:
				return True
		return False

# Create Admin
admin = Admin(app, name='RecordTrac Admin', url='/admin', index_view = HomeView(name='Home'))

class AdminView(ModelView):
    def is_accessible(self):
    	if current_user.is_authenticated():
			admins = app.config['LIST_OF_ADMINS'].split(",")
			if current_user.email.lower() in admins:
				return True
        return False

class RequestView(AdminView):
	can_create = False
	column_list = ('id', 'text', 'date_created', 'status') # The fields the admin can view
	column_searchable_list = ('status', 'text') # The fields the admin can search a request by
	form_excluded_columns = ('date_created', 'current_owner', 'extended', 'status', 'status_updated') # The fields the admin cannot edit.

class RecordView(AdminView):
	can_create = False
	column_searchable_list = ('description', 'filename', 'url', 'download_url', 'access')
	column_list = ('request_id', 'description', 'filename', 'url', 'download_url', 'access')
	can_edit = False

class QAView(AdminView):
	can_create = False
	column_list = ('request_id', 'question', 'answer', 'date_created')
	form_excluded_columns = ('date_created')

class NoteView(AdminView):
	can_create = False
	column_list = ('request_id', 'text', 'date_created')
	form_excluded_columns = ('date_created')

class UserView(AdminView):
	can_create = False
	column_list = ('id', 'contact_for', 'backup_for', 'alias')
	column_searchable_list = ('contact_for', 'alias')
	form_excluded_columns = ('date_created', 'department', 'password')

admin.add_view(RequestView(Request, db.session))
admin.add_view(RecordView(Record, db.session))
admin.add_view(NoteView(Note, db.session))
admin.add_view(QAView(QA, db.session))
admin.add_view(UserView(User, db.session))

# Routing dictionary.
routing = {
#   function_name: url
	'tutorial':{
		'url': '/tutorial'
	},
	'recaptcha':{
		'url': '/recaptcha',
		'methods':['GET', 'POST']
	},
	'landing':{
		'url': '/landing'
	},
	'unfollow':{
		'url': '/unfollow/<int:request_id>/<string:email>'
	},
	'index':{
		'url':'/',
		'methods':['GET', 'POST']
	},
	'explain_all_actions':{
		'url': '/actions'
	},
	'new_request': {
		'url': '/new',
		'methods': ['GET', 'POST']
	},
	'show_response':{
		'url': '/response/<int:request_id>'
	},
	'edit_case':{
		'url': '/edit/request/<int:request_id>'
	},
	'show_request_for_x':{
		'url': '/<string:audience>/request/<int:request_id>'
	},
	'show_request':{
		'url': '/request/<int:request_id>'
	},
	'track':{
		'url': '/track',
		'methods':['POST']
	},
	'viz': {
		'url': '/viz'
	},
	'docs': {
		'url': '/docs'
	},
	'any_page':{
		'url': '/<page>'
	},
	'requests':{
		'url': '/requests',
		'methods': ['GET', 'POST']
	},
	'update_password':{
		'url': '/update_password',
		'methods': ['GET', 'POST']
	},
	'logout':{
		'url': '/logout'
	},
	'login':{
		'url': '/login', 'methods': ['GET', 'POST']
	},
	'add_a_resource':{
		'url': '/add_a_<string:resource>',
		'methods': ['GET', 'POST']
	},
	'public_add_a_resource':{
		'url': '/public_add_a_<string:resource>',
		'methods': ['GET', 'POST']
	},
	'update_a_resource':{
		'url': '/update_a_<string:resource>',
		'methods': ['GET', 'POST']
	},
	'close':{
		'url': '/close',
		'methods': ['GET', 'POST']
	},
	'staff_card':{
		'url': '/staff_card/<int:user_id>'
	},
	'is_public_record':{
		'url': '/is_public_record',
		'methods': ['POST']
	},
	'reset_password':{
		'url': '/reset_password',
		'methods': ['POST']
	},
	'well_known_status': {
	    'url': '/.well-known/status',
	    'methods': ['GET']
	}
}


def route_url(function_name):
	methods = None
	if 'methods' in routing[function_name]:
		methods = routing[function_name]['methods']
	app.add_url_rule(routing[function_name]['url'], function_name, eval(function_name), methods = methods)

for function_name in routing:
	route_url(function_name)
