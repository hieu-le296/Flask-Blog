# blog_post/picture_handler.py

import os
from PIL import Image
from flask import url_for, current_app


def add_post_pic(pic_upload, title):
    filename = pic_upload.filename

    ext_type = filename.split('.')[-1]
    
    storage_filename = str(title) + ext_type

    filepath = os.path.join(current_app.root_path,
                            'static/posts/', storage_filename)
    output_size = (640, 640)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

   
    return storage_filename