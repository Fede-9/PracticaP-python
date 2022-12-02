class Config:
    SECRET_KEY = 'acapongocualquiercosa'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = '143.198.156.171'
    MYSQL_USER = 'BD2021'
    MYSQL_PASSWORD = 'BD2021itec'
    MYSQL_DB = 'blog'

    
config={
    'development':DevelopmentConfig
}