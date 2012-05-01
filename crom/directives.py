from grokker import Directive, ArgsDirective
from grokker import validator
from zope.interface import implementer

from .validators import (class_or_interface_validator, interface_validator)

source = ArgsDirective('adapts', 'crom',
                       validator=class_or_interface_validator)
target = Directive('provides', 'crom',
                   validator=interface_validator)
name = Directive('name', 'crom', validator=validator.str_validator)

# XXX expects either IRegistry or factory
registry = Directive('registry', 'crom')

implements = implementer

