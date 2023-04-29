from app import app

if __name__ == "__main__" :
    app.secret_key = "izzasecretkey"
    app.run(host='0.0.0.0',debug = True)