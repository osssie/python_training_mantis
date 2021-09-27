
def test_signup_new_account(app):
    username = 'test'
    password = '123456'
    app.james.ensure_user_exists(username, password)
