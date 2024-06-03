from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    '''Base class for configuraton'''
    SECRET_KEY = os.getenv('SECRET_KEY')

    # DB settings
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO_URI = os.getenv('MONGO_URI')

    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_INDEX_URL = os.getenv('PINECONE_INDEX_URL')


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
