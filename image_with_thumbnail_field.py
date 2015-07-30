# -*- encoding: utf-8 -*-

"""
Loosely based on "django-thumbs" by Antonio Melé
See: http://django.es and http://djangothumbnails.com
"""

PIC_FILES_PER_DIRECTORY = 10000 # Max files per directory.

# TODO: Add a method to re-create thumbs from raw images.
# TODO: Fix watermarking stuff

import io
import os

from PIL import Image
from math import floor

from django.core.files.base import ContentFile
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile

from django.conf import settings

# Make sure all watermark images exist.
#for k in settings.THUMBS_WATERMARK_IMAGES.keys():
#    f = settings.THUMBS_WATERMARK_IMAGES[k]
#    if not os.path.exists(f):
#        raise AssertionError('Watermark file not found "%s".' % f)

def calc_size(ow, oh, tw, th, resize_type='contain'):
    # ow: original image width, oh: original image height
    # tw: target width, th: target height.
    if resize_type == 'cover':
        # This one's easy because the image is cropped to the exact target size.
        w, h = tw, th
    elif resize_type == 'contain':
        # First calc to fit the width. Then check to see if height is still
        # to large, and if so, calc again to fit height.
        if ow > tw: oh = int(max(oh * tw / ow, 1)); ow = int(tw)
        if oh > th: ow = int(max(ow * th / oh, 1)); oh = int(th)
        w, h = ow, oh

    return (w, h)

def generate_thumb(img, thumb_size, format='JPEG'):
    """
    Generates a thumb image and returns a ContentFile object with the thumbnail.

    Parameters:
    img File object
    thumb_size The size_name, resize type, pic size, ie: ('thumb', 'cover', 200, 120)
      - size_name A short name for the size, only important for storage.
      - resize_type Either "cover" (maintain aspect ratio, fit into size and crop, so that size
            is completely covered) or "contain" (maintain aspect ratio and fit the complete
            image into size without cropping, may leave some blank space).
      - width Image width in pixels.
      - height Image height in pixels.
    format Not used, must be JPEG. XXXFormat of the original and thumbnail images ('jpeg','gif','png',...)
    """
    #if format.upper()=='JPG':
    format = 'JPEG'
    img.seek(0) # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(img)

    # Convert to RGB if necessary.
    if image.mode not in ('RGBA'): image = image.convert('RGBA')

    # Get desired size for thumbnail.
    size_name, resize_type, thumb_w, thumb_h = thumb_size

    # Orginal image size.
    xsize, ysize = image.size

    # Resize either "cover" or "contain".
    if resize_type == 'cover':

        w = int(thumb_w)
        h = int(max(ysize * thumb_w / xsize, 1))
        cx2, cy2 = 0, int((h - thumb_h) / 2) # part to crop
        if h < thumb_h:
            h = int(thumb_h)
            w = int(max(xsize * thumb_h / ysize, 1))
            cx2, cy2 = int((w - thumb_w) / 2), 0 # part to crop
        image = image.resize((w, h), Image.ANTIALIAS).crop((cx2, cy2, w-cx2, h-cy2))
        image.load() # Load is necessary after crop

    elif resize_type == 'contain':
        # First calc to fit the width. Then check to see if height is still
        # to large, and if so, calc again to fit height.
        #
        # thumb_w, thumb_h: this is the target.
        # xsize, ysize: this is the current situation.
        if xsize > thumb_w: ysize = int(max(ysize * thumb_w / xsize, 1)); xsize = int(thumb_w)
        if ysize > thumb_h: xsize = int(max(xsize * thumb_h / ysize, 1)); ysize = int(thumb_h)
        if (xsize, ysize) != (thumb_w, thumb_h):
            image = image.resize((xsize, ysize), Image.ANTIALIAS)

    else:
        raise ValueError('No such resize_type "{}".'.format(resize_type))

    # Maybe apply a watermark
    dim = '%dx%d' % (thumb_w, thumb_h)
    if dim in settings.THUMBS_WATERMARK_IMAGES.keys():
        watermark = Image.open(settings.THUMBS_WATERMARK_IMAGES[dim])
        if watermark.mode not in ('RGBA'):
            watermark = watermark.convert('RGBA')

        xsize, ysize = image.size
        xwm, ywm = watermark.size

        # Don't watermark images not equal requested size.
        if xsize == xwm and ysize == ywm:
            image.paste(watermark, None, watermark)

    # Save the new thumbnail.
    xio = io.BytesIO()
    image.save(xio, format)
    return ContentFile(xio.getvalue())

class ImageWithThumbsFieldFile(ImageFieldFile):
    """
    See ImageWithThumbsField for usage example
    """
    def __init__(self, *args, **kwargs):
        super(ImageWithThumbsFieldFile, self).__init__(*args, **kwargs)

        if self and self.field.sizes:
            for size in self.field.sizes:
                (size_name, resize_type, w, h) = size
                fp = self.get_filepath(size_name, self.name)
                setattr(self, 'url_{}'.format(size_name), os.path.join(settings.MEDIA_URL, fp))
                #rs = calc_size(self.width, self.height, w, h, resize_type)
                #setattr(self, 'width_{}'.format(size_name), rs[0])
                #setattr(self, 'height_{}'.format(size_name), rs[1])

    def recreate(self, name):
        """
        Re-create the thumbs for this image. 

        name The file name "12345.jpg" without path.
        """
        if not self.field.sizes:
            return False
        source_f = os.path.join(settings.MEDIA_ROOT, self.field.upload_to, name)
        with open(source_f, 'rb') as fh:
            for size in self.field.sizes:
                (size_name, resize_type, w, h) = size
                thumb_name = self.get_filepath(size_name, name)

                # Try to delete the thumb image file
                try: os.remove(os.path.join(settings.MEDIA_ROOT, thumb_name))
                except: pass

                thumb_content = generate_thumb(fh, size, 'jpg')
                thumb_name_ = self.storage.save(thumb_name, thumb_content)

                if thumb_name != thumb_name_:
                    print('Ahm, a file with this name already exists!')

    def save(self, name, content, save=True):
        super(ImageWithThumbsFieldFile, self).save(name, content, save)
        if self.field.sizes:
            for size in self.field.sizes:
                (size_name, resize_type, w, h) = size
                thumb_name = self.get_filepath(size_name, name)
                thumb_content = generate_thumb(content, size, 'jpg')
                thumb_name_ = self.storage.save(thumb_name, thumb_content)

                if thumb_name != thumb_name_:
                    # Ahm, a file with this name already exists!
                    pass

    def delete(self, save=True):
        name=self.name

        if self and self.field.sizes:
            for size in self.field.sizes:
                (size_name, resize_type, w, h) = size
                thumb_name = self.get_filepath(size_name, name)
                try:
                    self.storage.delete(thumb_name)
                except:
                    pass

        super(ImageWithThumbsFieldFile, self).delete(save)

    def get_filepath(self, size_name, name):
        # Returns the complete filename including path relative to MEDIA_ROOT.
        #
        # size_name A short name for the size. Used as sub directory name, as
        #   shortcut to get the URL of the image, etc.
        # name The filename set in the view, usually the database ID plus .jpg
        #
        try:
            xid = int(os.path.split(name)[1].rsplit('.', 1)[0])
            sub = str(int(floor(xid / PIC_FILES_PER_DIRECTORY)))
            fname = '{}.jpg'.format(xid)
            fp = os.path.join(size_name, sub, fname)
            return fp
        except ValueError:
            # This happens when "name" was empty because the file has not yet
            # been stored as a dataabse row and has no ID value yet.
            return ''


class ImageWithThumbsField(ImageField):
    attr_class = ImageWithThumbsFieldFile
    """
    Usage example:
    ==============
    photo = ImageWithThumbsField(upload_to='images', sizes=(
        (size_name, resize-type, 125, 125),('small', 'cover', 300, 200),)

        size_name: Sub directory inside the media directory for the resized image files.

        rezise-type: 'cover' resizes and then crops the image to fit dimentions.
                     'contain' Resized image to fit inside the dimentions with no crop.

    To retrieve image URL, exactly the same way as with ImageField:
        my_object.photo.url
    To retrieve thumbnails URL's just add the size to it:
        my_object.photo.url_125x125
        my_object.photo.url_300x200

    Note: The 'sizes' attribute is not required. If you don't provide it,
    ImageWithThumbsField will act as a normal ImageField

    How it works:
    =============
    For each size in the 'sizes' atribute of the field it generates a
    thumbnail with that size and stores it following this format:

    / media_dir / size_name / str(floor(DB_ID/10000)) / DB_ID . extension

    Following the usage example above: For storing a file called "photo.jpg"
    that is stored to the database with ID 37293 and receives a size_name = "s"
    is saved to: /media/s/3/37293.jpg

    """
    def __init__(self, verbose_name=None, name=None,
                 width_field=None, height_field=None, sizes=None, **kwargs):
        self.verbose_name=verbose_name
        self.name=name
        self.width_field=width_field
        self.height_field=height_field
        self.sizes = sizes
        super(ImageField, self).__init__(**kwargs)

