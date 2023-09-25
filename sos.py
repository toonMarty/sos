#!/usr/bin/env python3
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app, db
from flask_migrate import Migrate
from app.models.novice import Novice
from app.models.ticket import Ticket
from app.models.user import User
from app.models.role import Role, Permission


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def shell_context():
    return dict(db=db,
                Novice=Novice,
                Ticket=Ticket,
                User=User,
                Role=Role,
                Permission=Permission)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
