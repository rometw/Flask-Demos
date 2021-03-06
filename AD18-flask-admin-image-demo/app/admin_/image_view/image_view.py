import os
from flask_admin import expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView

from .image import _list_thumbnail, CustomImageUploadField


class ImageFileAdmin(FileAdmin):
    can_delete = False
    can_rename = False
    can_upload = False
    can_mkdir = False

    allowed_extensions = ('swf', 'jpg', 'gif', 'png')


class ImageView(ModelView):

    column_formatters = {
        'path': _list_thumbnail
    }

    form_columns = ('name', 'path')

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': CustomImageUploadField()
    }


class ImageModelView(ImageView):
    column_list = ('name', 'path')

    def __init__(self, *args, path, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    @expose('/download/<path:filename>')
    def download(self, filename):
        from flask import send_from_directory
        return send_from_directory(self.path, filename)
