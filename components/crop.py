#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image


class Crop():
    """
    Crop image
    """

    def description(self):
        """
        description returns a string describing what component does.
        """
        return "Crops the image with the specified arguments"

    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are
        used at design time to configure a components behaviour.
        For example an RSS reader component may get the url of the RSS feed and number of most 
        recent messages to display as attributes. attributes should return [(’url’,’string’),(’msgcount’,’int’)].
        """
        return [('left', 'int'),('top', 'int'),('width', 'int'), ('height', 'int'), ('center', 'str')]

    def __setitem__(self, key, item):
        if not (key == "left" or key == "top" or key == "width" or key == "height" or key == "center"):
            raise Exception(key + ' key is invalid')
        if key != "center" and not isinstance(item, int):
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
        dic = [
            ('crop', 'This method takes 4 arguments. First 2 arguments specifies the pixel that we started to crop. 3rd argument specifies the width of the new image while 4th one specifies the height.'),
            ('crop_on_center', 'This method takes 3 arguments. First 2 arguments specifies the width and the height of the new image. If the 3rd argument is True, image will be cropped from its center. Else it will be cropped from its left-top.')]

        return dic

    def crop_on_center(self,image):
        width = self.__getitem__('width')
        height = self.__getitem__('height')
        center = self.__getitem__('center')
        if center== 'True':
            image.crop(width=int(width), height=int(height), gravity= 'center')
        else:
            image.crop(0,0, width=int(width), height=int(height))
        return image

    def crop(self,image):
        left = self.__getitem__('left')
        right = self.__getitem__('right')
        width = self.__getitem__('width')
        height = self.__getitem__('height')
        image.crop(int(left), int(right), width=int(width), height=int(height))
        return image