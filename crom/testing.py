from .implicit import implicit
from . import monkey

def setup():
    monkey.incompat()
    implicit.initialize()

def teardown():
    monkey.revert_incompat()
    implicit.clear()
