__AUTHOR__ = "Tony"

from Expedia.airfare import search_flight
from utils import modifiers
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from utils.modifiers import choices_form
from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, SelectField, RadioField
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap(app)


class SearchForm(Form):
    param1 = StringField('Source', validators=[DataRequired()])
    param2 = StringField('Destination', validators=[DataRequired()])
    param3 = DateField('Pick a Date [y-m-d]', validators=[DataRequired()], id='Date')
    param4 = SelectField('Adults', choices=choices_form(6, 1), validators=[DataRequired()], default='1')
    param5 = SelectField('Children', choices=choices_form(5, 0), validators=[DataRequired()], default='0')
    check = RadioField('Select type of OUTPUT', validators=[DataRequired()],
                       choices=[('JSON', 'JSON'), ('Classic', 'Classic Web Response')])
    submit = SubmitField("Search")


@app.route('/', methods=["GET", "POST"])
def index():
    search_form = SearchForm(csrf_enabled=False)
    if search_form.validate_on_submit():
        return redirect(url_for('results', param1=str(search_form.param1.data), param2=str(search_form.param2.data),
                                param3=modifiers.format_date(str(search_form.param3.data)),
                                param4=str(search_form.param4.data), param5=str(search_form.param5.data),
                                check=str(search_form.check.data)))
    return render_template('index.html', form=search_form)


@app.route('/flights/source=<param1>dest=<param2>date=<param3>adult=<param4>child=<param5>type<check>?mode=s')
def results(param1, param2, param3, param4, param5, check):
    source = param1.upper()
    destination = param2.upper()
    date = param3
    adults = param4
    children = param5
    flight_results = search_flight()
    result_list = flight_results.flights(source, destination, date, adults, children)
    if check != 'JSON':
        if result_list != ValueError:
            return render_template("search_result.html", param1=source, param2=destination, param3=date,
                                   param4=adults, param5=children, result_list=result_list)

        else:
            return render_template("search_error.html", param1=source, param2=destination, param3=date, param4=adults,
                                   param5=children)
    if check == 'JSON':
        return jsonify(result_list)


if __name__ == '__main__':
    app.run(debug=False)