from flask import Flask, render_template, request

app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("login.html")
@app.route("/")
def home():
    return render_template("profile.html", isTopper=True, name="suraj", subjects=["MLP", "Stats", "MLT"])

@app.route("/submit" , methods=["POST"])
def submit():
    
    username = request.form.get("username")
    password = request.form.get("password")

    # if username == "prst" and password == "123" :

    valid_users = {
        "admin" : "123",
        "prst" : "2005",
        "suraj" : "1111"
    }
    if username in valid_users and password in valid_users[username]:
        return render_template("welcome.html", name = username)
    else:
        return "Invalid credentials"
    
if __name__ == "__main__":
    app.run(debug=True)