
from flask import Flask, render_template

from admin import admin
from user import user


app = Flask(__name__)
app.register_blueprint(admin, url_prefix="")
app.register_blueprint(user, url_prefix="")

# Home page route
@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)


    



    
   