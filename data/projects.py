from model.project import Project
import string
import random


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "*4
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata = [
    Project(name=random_string("name", 10), description=random_string("desc", 20))]