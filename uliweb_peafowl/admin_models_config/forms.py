from uliweb.form import *
from uliweb.i18n import ugettext_lazy as _
import logging

log = logging.getLogger(__name__)

class AddForm(Form):
    def form_validate(self, data):
        from uliweb.utils.common import import_attr, log
        from uliweb.orm import Model

        errors = {}

        if data['basemodel']:
            try:
                m = import_attr(data['basemodel'])
                if not (isinstance(m, type) and issubclass(m, Model)):
                    errors['basemodel'] = _("Object is not a subclass of Model")
            except Exception as e:
                log.exception(e)
                errors['basemodel'] = _("Model can't be imported")

        if data['extension_model']:
            try:
                m = import_attr(data['extension_model'])
                if not (isinstance(m, type) and issubclass(m, Model)):
                    errors['extension_model'] = _("Object is not a subclass of Model")
            except Exception as e:
                log.exception(e)
                errors['extension_model'] = _("Model can't be imported")

        return errors