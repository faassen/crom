import venusian
from zope.configuration.config import ConfigurationMachine

def grok(package, config):
    scanner = venusian.Scanner(config=config)
    scanner.scan(package)

def configure(package):
    config = ConfigurationMachine()
    grok(package, config)
    config.execute_actions()
    
    
