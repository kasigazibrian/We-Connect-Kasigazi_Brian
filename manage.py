"""manage.py to handle flask migrations"""
import unittest
from app import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    tests = unittest.TestLoader().discover('./testsv2', pattern='test*.py')
    test_result = unittest.TextTestRunner(verbosity=2).run(tests)
    if test_result.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == '__main__':
    manager.run()
