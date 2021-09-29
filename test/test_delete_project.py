from model.project import Project
from random import randrange


def test_delete_project(app):
    if app.project.count_projects() == 0:
        app.project.create(Project(name="to_delete"))
    old_projects = app.soap.get_project_list(app.config['webadmin']['username'], app.config['webadmin']['password'])
    index = randrange(len(old_projects))
    app.project.delete_project_by_index(index)
    new_projects = app.soap.get_project_list(app.config['webadmin']['username'], app.config['webadmin']['password'])
    assert len(old_projects) - 1 == len(new_projects)
