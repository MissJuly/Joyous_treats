from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, IntegerField, SubmitField, DecimalField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from src.shop.models import Product



# Create a form for product addition, subclassing FlaskForm
class ProductForm(FlaskForm):
    # Define form fields
    name = StringField("Product Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired(), NumberRange(min=0.01)])
    image = FileField("Image", validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images 0nly!')])
    availability = BooleanField("Availability", default=True)
    discount = IntegerField("Discount Percentage", validators=[NumberRange(min=0, max=100)])
    submit = SubmitField("Add Product")

# Create a form for search querying
class SearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Go")

