from app import create_app, db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    from app.models import Product, Category
    return {'db': db, 'Product': Product, 'Category': Category}