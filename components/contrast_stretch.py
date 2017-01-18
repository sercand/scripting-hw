#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image

class Contrast_stretch():
    """
    Run Functions
    """

    def description(self):
        """
        description returns a string describing what component does.
        """
        return "Enhance contrast of image by adjusting the span of the available colors."

    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are
        used at design time to configure a components behaviour.
        For example an RSS reader component may get the url of the RSS feed and number of most 
        recent messages to display as attributes. attributes should return [(’url’,’string’),(’msgcount’,’int’)].
        """
        return [('black', 'float', ['contrast_stretch']), ('white', 'float', ['contrast_stretch'])]

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
        dic = [('contrast_stretch', 'Using this method you can change the contrast values of the color pixels. First parameter is the black ratio and second parameter is the white ratio. If you select white as 1.0 you will maximize the contrast')]

        return dic

    def contrast_stretch(self,image):
        image.contrast_stretch(self.__getitem__('black'), self.__getitem__('white'))
        return image

