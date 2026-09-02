from dotenv import dotenv_values
from app import app
print (dotenv_values(".env"))

# config secret for csrf flask protection
app.config['SECRET_KEY'] = dotenv_values(".env")["SECRET_KEY"]


if __name__ == '__main__':
    print ('http://localhost:5000')
    app.run(host='0.0.0.0', port='5000')