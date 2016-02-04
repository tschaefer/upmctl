from ConfigParser import SafeConfigParser


def read_config(filename):
    config = SafeConfigParser()
    config.read(filename)
    return config


def get_basic_config(config):
    pass


def get_key_config(config):
    pass
