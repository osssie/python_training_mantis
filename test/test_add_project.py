from data.projects import testdata
import pytest


@pytest.mark.parametrize("project", testdata, ids=[repr(x) for x in testdata])
def test_add_project(app, project):
    old_projects = app.project.get_projects_list()
    app.project.create(project)
    new_projects = app.project.get_projects_list()
    old_projects.append(project)
    assert len(old_projects) == len(new_projects)
