import unittest
from flask_script import Manager
from app import APP
from waitress import serve
from app.main.db_utils import check_db
from app.main.config import CONFIG


manager = Manager(app=APP)


@manager.command
def run():
    ''' Run application comman '''
    check_db()
    if CONFIG.API_ENV == "prod":
        serve(app=APP, host=CONFIG.HOST, port=CONFIG.PORT)
    else:
        APP.run(host=CONFIG.HOST, port=CONFIG.PORT)


@manager.command
def test():
    ''' Runs the unit tests. '''
    tests = unittest.TestLoader().discover('app/test', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
