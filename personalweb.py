from app import create_app, cli, db
from app.models import User, Prediction

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Prediction': Prediction}
