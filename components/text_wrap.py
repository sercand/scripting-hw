#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

class Text_wrap():
    """
    Run Functions
    """

    def description(self):
        """
        description returns a string describing what component does.
        """
        return "Wraps a string into the image with specified position and color"

    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are
        used at design time to configure a components behaviour.
        For example an RSS reader component may get the url of the RSS feed and number of most 
        recent messages to display as attributes. attributes should return [(’url’,’string’),(’msgcount’,’int’)].
        """
        return [('color', 'str', ['text_wrap']),('font_size', 'int', ['text_wrap']), ('width_place', 'float', ['text_wrap']), ('height_place', 'float', ['text_wrap']), ('quote', 'str', ['text_wrap'])]

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
        dic = [('text_wrap', 'Using this method you can wrap a text into the image. To do this you should provide text color, text font size, where to put the text and the text you want to wrap')]

        return dic

    def text_wrap(self,image):
        draw = Drawing()
        draw.font = 'wandtests/assets/League_Gothic.otf'
        draw.fill_color = Color(self.__getitem__('color'))
        draw.text_alignment = 'center'
        image.font_size = self.__getitem__('font_size')
        draw.text(int(self.__getitem__('width_place')*image.width), int(self.__getitem__('height_place')*image.height), self.__getitem__('quote'))
        draw(image)
        return image


