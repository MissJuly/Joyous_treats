from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TelField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from src.accounts.models import User


# Create a form for user registration, subclassing FlaskForm
class RegisterForm(FlaskForm):
    # Define form fields with corressponding validators
    name = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])
    email = EmailField("Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    phone_number = TelField("Phone Number", validators=[Length(max=16)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=25)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Password must match!")])

    # Custom validation method for the form data
    def validate(self, extra_validators=None):
        # Perform initial validation using the built-in FlaskForm validation
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:   # If initial validation fails, return False
            return False

        # Check if a user with the provided email already exists in the database
        user = User.query.filter_by(email=self.email.data).first()
        if user:  # If a user with this email exists, add an error message and return False
            self.email.errors.append("Email already exists!")
            return False

        # Check if the password and confirm password fields match
        if self.password.data != self.confirm.data:
            self.password.errors.append("Password must match!")
            return False

        # If all validations pass, return true to indicate successsful validation
        return True


# Create a form for user login, also subclassing FlaskForm
class LoginForm(FlaskForm):
    # Define form fields with the corresponding validators
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

