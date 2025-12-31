from flask import Flask, request, redirect, flash, url_for, render_template
from forms import RegistrationForm

app = Flask(__name__)
app.secret_key = "my-secret-key"

@app.route("/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        flash(f"Welcome {name}. you register successfuly !!", "success")
        return redirect(url_for("success", name=name))
    return render_template("register.html", form=form)

@app.route("/success/<name>")
def success(name):
    return render_template("success.html",name=name )