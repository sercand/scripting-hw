#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image


class Fx():
    """
    Run Functions
    """

    def description(self):
        """
        description returns a string describing what component does.
        """
        return "fx"

    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are
        used at design time to configure a components behaviour.
        For example an RSS reader component may get the url of the RSS feed and number of most 
        recent messages to display as attributes. attributes should return [(’url’,’string’),(’msgcount’,’int’)].
        """
        return [('adj', 'int')]

    def __setitem__(self, key, item):
        #        if not (key == "width" or key == "height"):
        #            raise Exception(key + ' key is invalid')
        #        if not isinstance(item, int):
        #            raise Exception(key + ' is invalid type')
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
        dic = [('level', 'Black & white boundaries of an image can be controlled with level methodSimilar to the gamma() method, mid-point levels can be adjusted with the gamma keyword argument'),
               ('gamma', 'Gamma correction allows you to adjust the luminance of an image. Resulting pixels are defined as pixel^(1/gamma). The value of gamma is typically between 0.8 & 2.3 range, and value of 1.0 will not affect the resulting image.')]

        return dic

    def level(self, image):
        image.level(0.2, 0.8, gamma=self.__getitem__('adj'))
        return image

    def gamma(self, image):
        image.gamma(self.__getitem__('adj'))
        return image
