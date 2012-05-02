from grokker import validator
from zope.interface.interfaces import IInterface

def isinterface(value):
    return IInterface.providedBy(value)

def interface_validator(directive_name, value):
    if not isinterface(value):
        raise validator.GrokkerValidationError(
            "the '%s' directive can only be called with an interface." %
            directive_name)

def class_or_interface_validator(directive_name, value):
    if (not validator.isclass(value) and
        not isinterface(value)):
        raise validator.GrokkerValidationError(
            "The '%s' directive can only be called with a "
            "class or an interface." % directive_name)


        
