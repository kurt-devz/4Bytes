import io
import csv
import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, File, Data
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, getAllFiles )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

@app.cli.command("listFiles", help="Lists all files in the database")
def listFiles():
    print(getAllFiles())

@app.cli.command("file-data", help="Creates a user")
def print_file_data():
    file = File.query.filter_by(id=1).first()
    if file is None:
        print("File not found")
        return
    print(f'File name: {file.name}')
    csv_file_like = io.StringIO(file.fileData.decode('utf-8'))
    reader = csv.reader(csv_file_like)
    for row in reader:
        print(row)




'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Data Commands
'''
@app.cli.command("data", help="Lists all data in the database")
def create_data_command():
    data = Data.query.all()
    print(data)

@app.cli.command("list-data", help="Lists all data in the database")
def list_data_command():
    data = Data.query.all()
    if not data:
        print("No data found")
        return
    for d in data:
        print(f"Data: {d.id} {d.gradute}, {d.fauculty}, {d.programme}, {d.age}")
'''
Test Commands
'''
test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

