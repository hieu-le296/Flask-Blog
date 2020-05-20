# blog_posts/post_image.py

import os
from PIL import Image
from flask import url_for, current_app


def add_post_pic(pic_upload, title):
    filename = pic_upload.filename
    # "mypicture.jpg"
    # "username.jpg"
    filepath = os.path.join(current_app.root_path,
                            'static/posts', filename)
    output_size = (800, 800)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    #title.png
    return filename


