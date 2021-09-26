# -*- coding: utf-8 -*-
from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        wd.find_element_by_css_selector(".fa-gears").click()
        wd.find_element_by_link_text(u"Управление проектами").click()

    def create(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_xpath("//button[@type='submit']").click()
        self.fill_project_form(project)
        wd.find_element_by_css_selector("input.btn").click()
        wd.find_element_by_link_text(u"Продолжить").click()
        self.project_cache = None

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_data("project-name", project.name)
        self.change_field_data("project-description", project.description)

    def change_field_data(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_id(field_name).click()
            wd.find_element_by_id(field_name).clear()
            wd.find_element_by_id(field_name).send_keys(text)

    def count_projects(self):
        wd = self.app.wd
        self.open_project_page()
        return len(wd.find_elements_by_xpath("//div[2]/table/tbody/tr"))

    def get_projects_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_project_page()
            self.project_cache = []
            for row in wd.find_elements_by_xpath("//div[2]/table/tbody/tr"):
                cells = row.find_elements_by_tag_name("td")
                link = row.find_element_by_css_selector("a").get_attribute('href')
                id = link[link.find("=") + 1:]
                name = cells[0].text
                description = cells[4].text
                scanned_project = Project(id=id, name=name, description=description)
                self.project_cache.append(scanned_project)
            return list(self.project_cache)

    def select_project_by_index(self, index):
        wd = self.app.wd
        selected_project = wd.find_elements_by_xpath("//div[2]/table/tbody/tr")[index]
        selected_project.find_element_by_xpath("./td[1]/a").click()

    def delete_project_by_index(self, index):
        wd = self.app.wd
        self.open_project_page()
        self.select_project_by_index(index)
        wd.find_element_by_xpath("//input[@value='Удалить проект']").click()
        wd.find_element_by_xpath("//input[@value='Удалить проект']").click()
        self.project_cache = None

    project_cache = None
