from app import app

@app.route('/')
def index():
    return "<b>Hello</b>"