#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image

class Gaussian_blur():
    """
    Run Functions
    """

    def description(self):
        """
        description returns a string describing what component does.
        """
        return "Blurs the image."

    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are
        used at design time to configure a components behaviour.
        For example an RSS reader component may get the url of the RSS feed and number of most 
        recent messages to display as attributes. attributes should return [(’url’,’string’),(’msgcount’,’int’)].
        """
        return [('radius', 'float', ['gaussian_blur']), ('sigma', 'float', ['gaussian_blur'])]

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
        dic = [('gaussian_blur', 'Convolve the image with a gaussian operator of the given radius and standard deviation (sigma). For reasonable results, the radius should be larger than sigma.')]

        return dic

    def gaussian_blur(self,image):
        image.gaussian_blur(self.__getitem__('radius'), self.__getitem__('sigma'))
        return image

