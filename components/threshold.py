#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image


class Threshold():
    """
    Threshold image
    """

    def description(self):
        """
        description returns a string describing what component does.
        """
        return "Changes the value of individual pixels based on the intensity of each pixel compared to threshold. The result is a high-contrast, two color image. It manipulates the image in place."

    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are
        used at design time to configure a components behaviour.
        For example an RSS reader component may get the url of the RSS feed and number of most 
        recent messages to display as attributes. attributes should return [(’url’,’string’),(’msgcount’,’int’)].
        """
        return [('factor', 'float'), ('channel', 'str')]

    def __setitem__(self, key, item):
        if not (key == "factor" or key == "channel"):
            raise Exception(key + ' key is invalid')
        if key != "channel" and not isinstance(item, float):
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
            ('threshold', 'This method takes 2 arguments. First one is a float number between 0.0 and 1.0. It is the threshold factor. Second argument is the channel for the image. This channel could be one of these strings: red, green, cyan, gray, magenta, blue, yellow, alpha, black, opacity, true_alpha, sync_channels, gray_channels and composite_channels')
                ]

        return dic

    def threshold(self,image):
        thr = self.__getitem__('factor')
        chn = self.__getitem__('channel')
        image.threshold(thr, chn)
        return image 