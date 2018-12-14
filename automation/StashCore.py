#
import requests

from automation import JenkinsCore


class StashCore:

    def __init__(self, jenkins: JenkinsCore = None, debug: bool = None):
        self.debug = debug
        self.jenkins = jenkins
        self.b_url = 'https://{0}:{1}@stash.pontoslivelo.com.br/rest/api/1.0'\
            .format(self.jenkins.get_user(), self.jenkins.get_passwd())
        pass

    def get_all_projects(self):
        #
        data = dict(limit=500)

        #
        response = requests.get(url='{0}/projects'.format(self.b_url), params=data)
        return response.json()

    def get_project_name(self, project_id: str = None):
        #
        data = self.get_all_projects()
        project_id = project_id.upper()

        for project in data['values']:
            if project['key'] == project_id:
                return project['name']
            continue
        return None

    def validate(self):
        pass

    def analise_content(self):
        pass