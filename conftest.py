import pytest
import os.path
import json
import ftputil
from fixture.application import Application


fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as file:
            target = json.load(file)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, baseurl=config["web"]["baseUrl"])
        fixture.session.ensure_login(username=config["webadmin"]["username"], password=config["webadmin"]["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])

    def fin():
        restore_server_configuration(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.php.bak"):
            remote.remove("config_defaults_inc.php.bak")
        if remote.path.isfile("config_defaults_inc.php"):
            remote.rename("config_defaults_inc.php", "config_defaults_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_defaults_inc.php"), "config_defaults_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.php.bak"):
            if remote.path.isfile("config_defaults_inc.php"):
                remote.remove("config_defaults_inc.php")
            remote.rename("config_defaults_inc.php.bak", "config_defaults_inc.php")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.tearDown()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="config/target.json")
    # parser.addoption("--check_ui", action="store_true")


# @pytest.fixture(scope="session")
# def orm(request):
#     db_config = load_config(request.config.getoption("--target"))['db']
#     dbfixture = ORMFixture(host=db_config["host"], name=db_config["name"], user=db_config["user"],
#                            password=db_config["password"])

    # def fin():
    #     dbfixture.destroy()
    # request.addfinalizer(fin)


# @pytest.fixture(scope="session")
# def db(request):
#     db_config = load_config(request.config.getoption("--target"))['db']
#     dbfixture = DbFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'],
#                           password=db_config['password'])
#
#     def fin():
#         dbfixture.destroy()
#     request.addfinalizer(fin)
#     return dbfixture
#
#
# @pytest.fixture
# def check_ui(request):
#     return request.config.getoption("--check_ui")
#
#
# def pytest_generate_tests(metafunc):
#     for fixture in metafunc.fixturenames:
#         if fixture.startswith("data_"):
#             testdata = load_from_module(fixture[5:])
#             metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
#         elif fixture.startswith("json_"):
#             testdata = load_from_json(fixture[5:])
#             metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
#
#
# def load_from_module(module):
#     return importlib.import_module("data.%s" % module).testdata
#
#
# def load_from_json(file):
#     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
#         return jsonpickle.decode(f.read())
