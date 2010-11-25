from attest import Tests

from tests.rendering import rendering
from tests.filters import filters
from tests.context_processors import contexts
from tests.strings import strings
from tests.module_templates import modules
from tests.jinja_tests_and_filters import jinja
from tests.i18n import i18n
from tests.signals import signals


all = Tests([rendering,
             filters,
             contexts,
             strings,
             modules,
             jinja,
             i18n,
             signals,
            ])
