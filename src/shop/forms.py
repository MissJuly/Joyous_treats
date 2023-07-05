from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DecimalField, BooleanField, TextAreaField
from wtforms.validators import DataRequired
from src.shop.models import Product



# Create a form for product addition, subclassing FlaskForm
class ProductForm(FlaskForm):
    # Define form fields
    product_name = StringField("Product Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[DataRequired()])
    availability = BooleanField("Availability", validators=[DataRequired()])
    discount = IntegerField("Discount", validators=[DataRequired()])
    submit = SubmitField("Add Product")



