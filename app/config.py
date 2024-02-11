import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEVELOPMENT = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY', 'TzmGM"Zk_m0$ivf>Cp:9)yThG/fscg')

    API_KEY = os.environ.get('API_KEY', "6930eb1e-4587-4e5d-934d-60e9adcb5d5f")

    