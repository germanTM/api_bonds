from app import app
from app import blueprint


app.register_blueprint(blueprint)
app.app_context().push()

app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////main/bonds_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5000, debug=True, threaded = True)

