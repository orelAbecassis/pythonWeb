import os
import pytest
from app import app, db, Person

@pytest.fixture
def client():
    # Configure une base de données de test
    app.config['TESTING'] = True

    # Définir la variable d'environnement pour TEST_DATABASE_URL si elle n'existe pas
    if 'TEST_DATABASE_URL' not in os.environ:
        os.environ['TEST_DATABASE_URL'] = 'sqlite:///:memory:'

    # Utiliser TEST_DATABASE_URL pour configurer SQLAlchemy
    test_database_url = os.getenv('TEST_DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = test_database_url

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create database tables for testing
            yield client
            db.drop_all()  # Drop tables after testing

def test_homepage(client):
    """Test that the homepage loads correctly."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'<!DOCTYPE html>' in rv.data  # Assuming your HTML template starts with <!DOCTYPE html'

def test_generate_fake_data(client):
    """Test that fake data is generated correctly."""
    with app.app_context():
        initial_count = Person.query.count()
        assert initial_count == 0  # Ensure the database is empty initially

        from app import generate_fake_data
        generate_fake_data()

        new_count = Person.query.count()
        assert new_count == 100  # Ensure 100 fake persons are added
