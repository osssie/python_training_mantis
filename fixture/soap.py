from model.project import Project
from suds.client import Client
from suds import WebFault


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.base_url + "/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self):
        client = Client(self.app.baseurl + "/api/soap/mantisconnect.php?wsdl")
        username, password = (self.app.config['webadmin']['username'], self.app.config['webadmin']['password'])
        try:
            projects = client.service.mc_projects_get_user_accessible(username, password)
            res = []
            for project in projects:
                res.append(Project(id=str(project.id), name=str(project.name), status=str(project.status.name),
                                   view_state=str(project.view_state.name), description=str(project.description),
                                   active=project.enabled))
            return res
        except WebFault:
            return False
