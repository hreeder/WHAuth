#!/usr/bin/env python
from flask.ext.assets import ManageAssets
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager

from auth import app, assets

manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()