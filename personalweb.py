from app import app, cli, db
from app.models import User, Prediction


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Prediction': Prediction}
