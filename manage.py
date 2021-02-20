import unittest
from test_helper import create_app
from flask_script import Manager, Shell


app = create_app("testing")
manager = Manager(app)


def make_shell_context():
    return dict(app=app)
manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def run_test():
    print("Start testing.")
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)


if __name__ == "__main__":
    manager.run()
