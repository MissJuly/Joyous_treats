from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TelField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from src.accounts.models import User


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])
    email = EmailField("Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    phone_number = TelField("Phone Number", validators=[Length(max=16)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=25)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Password must match!")])

    # validates data
    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators) # validates using FlaskForm
        if not initial_validation:
            return False

        user = User.query.filter_by(email=self.email.data).first() # custom validation
        if user:
            self.email.errors.append("Email already exists!") # checks if user is registered
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Password must match!") # checks if passwords match
            return False
        return True


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

