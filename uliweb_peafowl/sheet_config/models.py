#coding=utf-8
from uliweb.orm import *
from uliweb.utils.common import get_var
from uliweb.i18n import ugettext_lazy as _

def get_modified_user():
    from uliweb import request
    return request.user.id

class Sheet_Config(Model):
    sheet_name = Field(str, verbose_name=_('表单名称'), unique=True)
    display_name = Field(str, verbose_name=_('显示名称'))
    description = Field(str, verbose_name=_('描述'), max_length=255)
    uuid = Field(CHAR, verbose_name=_('UUID'), max_length=32)
    modified_user = Reference('user', verbose_name=_('修改人'), default=get_modified_user, auto_add=True, auto=True)
    modified_time = Field(datetime.datetime, verbose_name=_('修改时间'), auto_now=True, auto_now_add=True)
    published_time = Field(datetime.datetime, verbose_name=_('生效时间'))
    version = Field(int)

    def __unicode__(self):
        return "%s(%s)" % (self.sheet_name, self.uuid)

    def get_instance(self):
        SCH = get_model('sheet_config_his', signal=False)
        return SCH.get(SCH.c.uuid==self.uuid)

class Sheet_Config_His(Model):
    sheet_name = Field(str, verbose_name=_('表单名称'), unique=True, required=True)
    display_name = Field(str, verbose_name=_('显示名称'))
    description = Field(str, verbose_name=_('描述'), max_length=255)
    uuid = Field(CHAR, verbose_name=_('UUID'), max_length=32, index=True)
    basemodel = Field(str, verbose_name=_('关联Model名称'))    
    layout = Field(TEXT)
    fields = Field(TEXT)
    version = Field(int)
    status = Field(CHAR, max_length=1, verbose_name=_('是否生效'),
                   choices=get_var('SHEETCONFIG_SETTING/STATUS'), default='0')
    modified_user = Reference('user', verbose_name=_('修改人'), default=get_modified_user, auto_add=True, auto=True)
    modified_time = Field(datetime.datetime, verbose_name=_('修改时间'), auto_now=True, auto_now_add=True)
    create_time = Field(datetime.datetime, verbose_name=_('创建时间'), auto_now_add=True)
    published_time = Field(datetime.datetime, verbose_name=_('生效时间'))

    def sync(self):
        SC = get_model('sheet_config')
        data = {
            'sheet_name': self.sheet_name,
            'display_name': self.display_name,
            'description' : self.description,
        }

        obj = SC(**data)
        obj.save(version=True)

