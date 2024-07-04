import os
import pytest
from app import app, db, Person


@pytest.fixture
def client():
    # Configure une bdd de test
    app.config['TESTING'] = True
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
    assert b'<!DOCTYPE html>' in rv.data  # Assuming your HTML template starts with <!DOCTYPE html>


def test_generate_fake_data(client):
    """Test that fake data is generated correctly."""
    with app.app_context():
        initial_count = Person.query.count()
        assert initial_count == 0  # Ensure the database is empty initially

        from app import generate_fake_data
        generate_fake_data()

        new_count = Person.query.count()
        assert new_count == 100  # Ensure 100 fake persons are added
