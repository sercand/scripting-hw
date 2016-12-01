#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image


class Resize():
    """
    Resize image
    """

    def description(self):
        """
        description returns a string describing what component does.
        """
        return "resizes the image"

    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are
        used at design time to configure a components behaviour.
        For example an RSS reader component may get the url of the RSS feed and number of most 
        recent messages to display as attributes. attributes should return [(’url’,’string’),(’msgcount’,’int’)].
        """
        return [('width', 'int'), ('height', 'int'), ('ratio', 'int')]

    def __setitem__(self, key, item):
        if not (key == "width" or key == "height" or key == "ratio"):
            raise Exception(key + ' key is invalid')
        if not isinstance(item, int):
            raise Exception(key + ' is invalid type')
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def methods(self):
        """
        methods return a list of method calls and their descriptions. The methods define the behaviour of the 
        component at execution time. This way, application can interact with the components. RSS reader 
        can return [(’getpage’, ’Changes␣current␣page␣to␣given␣page␣no’)] so that user can go to arbitrary
        pages on reader. getpage() should be implemented on the RSS reader componentclass.
        """
        dic = [('resize_width', 'This method resizes the image width and it takes 3 parameters. As a first parameter provide the image you get with the path or url. As the second parameter provide the width you want to resize the image. As the last parameter provide the image name you want to save after image resize operation')]
        dic = dic + [('resize_height', 'This method resizes the image height and it takes 3 parameters. As a first parameter provide the image you get with the path or url. As the second parameter provide the height you want to resize the image. As the last parameter provide the image name you want to save image after resize operation')]
        dic = dic + [('resize_with_value', 'This method resizes the image width and height and it takes 4 parameters. As a first parameter provide the image you get with the path or url. As the second parameter provide the width you want to resize the image. As the third parameter provide the height you want to resize the image. As the last parameter provide the image name you want to save image after resize operation')]
        dic = dic + [('resize_with_ratio', 'This method resizes the image width and height and it takes 4 parameters. As a first parameter provide the image you get with the path or url. As the second parameter provide a ratio as float to multiply with the width. As the third parameter provide a ratio as float to multiply with the height. As the last parameter provide the image name you want to save image after resize operation')]

        return dic

    def resize_with_ratio(self, image):
        ratio = self.__getitem__('ratio')
        image.resize(int(image.width * ratio), int(image.height * ratio))
        self.exec_image = image
        return image

    def resize_with_value(self, image):
        image.resize(self.__getitem__('width'), self.__getitem__('height'))
        return image

    def resize_width(self, image):
        image.resize(self.__getitem__('width'), image.height)
        return image

    def resize_height(self, image):
        image.resize(image.width, self.__getitem__('height'))
        return image


if __name__ == "__main__":
    resize = Resize()
