from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


class FuncDataForm(FlaskForm):
    func = StringField('Функция:',
                       validators=[DataRequired(message='Заполните все поля')])
    a = StringField('Левая граница:',
                    validators=[DataRequired(message='Заполните все поля')])
    b = StringField('Правая граница',
                    validators=[DataRequired(message='Заполните все поля')])
    eps = StringField('Погрешность:',
                      validators=[DataRequired(message='Заполните все поля')],
                      default='1e-6')
    submit = SubmitField('Рассчитать!')


def bisection(f, a, b, eps=1e-6):
    if f(a) * f(b) >= 0:
        raise ValueError("Функция не меняет знак на отрезке [a, b].")
    progress_lst = []
    while (b - a) / 2 > eps:
        k = (a + b) / 2
        progress_lst.append([f'[{"+" if f(a) > 0 else "-"}{a}:{"+" if f(k) > 0 else "-"}{k}]',
                             f'[{"+" if f(k) > 0 else "-"}{k}:{"+" if f(b) > 0 else "-"}{b}]'])
        if f(k) == 0:
            return k, progress_lst
        elif f(a) * f(k) < 0:
            b = k
            progress_lst[-1].append('r')
        else:
            a = k
            progress_lst[-1].append('l')

    return (a + b) / 2, progress_lst


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FuncDataForm()
    if form.validate_on_submit():
        f = lambda x: eval(form.func.data)
        a = float(form.a.data)
        b = float(form.b.data)
        eps = float(form.eps.data)
        try:
            root, progress = bisection(f, a, b, eps)
            return render_template('index.html', root=root, form=form, progress_lst=progress)
        except ValueError as e:
            return render_template('index.html', error=e, form=form)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
