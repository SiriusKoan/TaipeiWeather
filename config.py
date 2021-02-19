class DevelopmentConfig:
    ENV = "development"
    DEBUG = True


class TestingConfig:
    ENV = "testing"
    TESTING = True


class ProductionConfig:
    ENV = "production"


config_list = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
