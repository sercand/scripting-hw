#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image
import pprint

class Flip_Flop():
    """
    Crop image
    """

    def description(self):
        """
        description returns a string describing what component does.
        """
        return "Using flip, user can create a vertical mirror of the image by rotating the pixels around x-axis. With flop, user can create a horizontal mirror of the image by rotating the pixels around y-axis."

    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are
        used at design time to configure a components behaviour.
        For example an RSS reader component may get the url of the RSS feed and number of most 
        recent messages to display as attributes. attributes should return [(’url’,’string’),(’msgcount’,’int’)].
        """
        return []

    def __setitem__(self, key, item):
        None

    def __getitem__(self, key):
        None

    def methods(self):
        """
        methods return a list of method calls and their descriptions. The methods define the behaviour of the 
        component at execution time. This way, application can interact with the components. RSS reader 
        can return [(’getpage’, ’Changes␣current␣page␣to␣given␣page␣no’)] so that user can go to arbitrary
        pages on reader. getpage() should be implemented on the RSS reader componentclass.
        """
        dic = [
            ("flip", "Flip method takes no argument. Using flip method you can create a mirror image by rotating the pixels around x-axis"),
            ("flop", "Flop method takes no argument. Using flop method you can create a mirror image by rotating the pixels around y-axis")]

        return dic

    def flip(self,image):
        image.flip()
        return image

    def flop(self,image):
        image.flop()
        return image