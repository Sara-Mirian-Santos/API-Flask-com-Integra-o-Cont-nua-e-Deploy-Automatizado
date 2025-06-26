import os
from app import app
from flaskext.mysql import MySQL

mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_USER', 'sqlite:///default.db')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'sqlite:///default.db')
app.config['MYSQL_DATABASE_DATABASE'] = os.getenv('MYSQL_DATABASE', 'sqlite:///default.db')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_HOST', 'sqlite:///default.db')
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)