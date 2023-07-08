from datetime import datetime
from flask.cli import FlaskGroup
from src import app, db
from src.accounts.models import User
import getpass


cli = FlaskGroup(app)


@cli.command("create_admin")
def create_admin():
   """Create admin"""
   name = input("Enter name: ")
   email = input("Enter email address: ")
   password = getpass.getpass("Enter the password: ")
   confirm_password = getpass.getpass("Confirm password: ")

   if password != confirm_password:
      print("Passwords don't match!")
      return 1
   try:
      current_time = datetime.now()

      user = User(name=name,
                  email=email,
                  password=password,
                  phone_number=None,
                  is_admin=True,
                  created_at=current_time,
                  updated_at=current_time)

      db.session.add(user)
      db.session.commit()

      print("Admin successfully added.")

   except Exception:
      print("Admin user creation failed!!")


if __name__ == "__main__":
   cli()
