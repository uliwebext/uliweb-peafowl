#coding=utf8
from uliweb import expose, functions
import logging

log = logging.getLogger(__name__)

@expose('/library_demo/webuploader')
def webuploader():
    response.template = 'LibraryDemoView/webuploader.html'

    return {}


@expose('/library_demo/fileupload')
def fileupload():
    from uliweb.form import Form, FileField
    class UploadForm(Form):
        filename = FileField()

    form = UploadForm()
    flag = form.validate(request.values, request.files)
    if flag:
        filename = functions.save_file_field(form.filename)
        print request.values, request.files
        url = functions.get_href(filename)
        return json({'success':True, 'filename':filename, 'url':url})
    else:
        #如果校验失败，则再次返回Form，将带有错误信息
        return json({'success':False, 'errors':form.errors})

@expose('/library_demo/filedelete/<path:filename>')
def filedelete(filename):
    try:
        functions.delete_filename(filename)
        return json({'success':True, 'message':'Delete success.'})
    except Exception as e:
        log.exception(e)
        return json({'success':False, 'message':'Delete file error'})