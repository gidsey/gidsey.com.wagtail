import pytest


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def test_email():
    return 'test@gidsey.com'


@pytest.fixture
def test_username():
    return 'testusername'


@pytest.fixture
def create_user(db, django_user_model, test_password, test_email, test_username):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        kwargs['is_staff'] = False
        kwargs['is_superuser'] = False
        if 'username' not in kwargs:
            kwargs['username'] = test_username
        if 'email' not in kwargs:
            kwargs['email'] = test_email
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login

