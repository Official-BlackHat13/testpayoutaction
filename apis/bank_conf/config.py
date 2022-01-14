import configparser

class Configuration():
    config = configparser.ConfigParser()
    config.read('apis/bank_conf/config.ini')
    env = config.get(config.sections()[0], 'Environment')
    
    def get_Property(key):
        return Configuration.config.get(Configuration.env, key)
