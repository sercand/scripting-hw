#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image
from wand.color import Color


class Rotate():
    """
    Rotate
    """

    def description(self):
        """
        description returns a string describing what component does.
        """
        return "rotates the image with specified degree"

    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are
        used at design time to configure a components behaviour.
        For example an RSS reader component may get the url of the RSS feed and number of most 
        recent messages to display as attributes. attributes should return [(’url’,’string’),(’msgcount’,’int’)].
        """
        return [('degree', 'int'), ('background', 'str')]

    def __setitem__(self, key, item):
        if not (key == "degree" or key == "background"):
            raise Exception(key + ' key is invalid')
        if key == "degree" and not isinstance(item, int):
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
        dic = [('rotate', 'This method takes 1 parameter. User will provide a degree to rotate the image with. The background color will be transparent by default.Rotation value must be integer'), ('rotate_with_background',
                                                                                                                                                                                                      'This method takes 2 parameters. First parameter will be the degree to rotate the image with and the second parameter will be the background color. Rotation value must be integer and the background color is a string that specifies the RGB value such as:(#f00)')]

        None

    def rotate(self, image):
        degree = self.__getitem__('degree')
        image.rotate(degree)
        return image

    def rotate_with_background(self, image):
        degree = self.__getitem__('degree')
        background = self.__getitem__('background')
        c = Color(background)
        image.rotate(degree, c)
        return image
