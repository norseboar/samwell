from app import app

@app.route('/')
def home():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
