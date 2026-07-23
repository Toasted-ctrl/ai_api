from core.config import config, ApplicationConfig

def test_applications():

    apps = config.APPLICATIONS

    # Verify admin settings

    assert "admin" in apps

    admin = apps.get("admin", None)

    assert isinstance(admin, ApplicationConfig)

    assert admin.name
    assert admin.api_key
    assert admin.hmac_secret

    assert isinstance(admin.require_google_id, bool)
    assert isinstance(admin.require_jwt, bool)
    assert isinstance(admin.hmac_secret, bytes)


    # Verify JELAIME settings
    
    assert "jelaime" in apps

    jelaime = apps.get("jelaime", None)

    assert isinstance(jelaime, ApplicationConfig)

    assert jelaime.name
    assert jelaime.api_key
    assert jelaime.hmac_secret
    assert jelaime.require_google_id
    assert jelaime.require_jwt

    assert isinstance(jelaime.hmac_secret, bytes)


def test_db_url():

    assert isinstance(config.PG_DB_URL, str)