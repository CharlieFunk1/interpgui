from app import app, db
from app.models import Strip, Configure

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Strip': Strip, 'Configure': Configure}

