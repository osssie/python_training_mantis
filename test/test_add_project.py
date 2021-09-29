from data.projects import testdata
import pytest


@pytest.mark.parametrize("project", testdata, ids=[repr(x) for x in testdata])
def test_add_project(app, project):
    old_projects = app.soap.get_project_list(app.config['webadmin']['username'], app.config['webadmin']['password'])
    app.project.create(project)
    new_projects = app.soap.get_project_list(app.config['webadmin']['username'], app.config['webadmin']['password'])
    old_projects.append(project)
    assert len(old_projects) == len(new_projects)
