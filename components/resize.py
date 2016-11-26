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
        return [('width', 'int'), ('height', 'int')]

    def __setitem__(self, key, item):
        if not (key == "width" or key == "height"):
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
        return [('resize', 'Resizes the image')]

    def execute(self):
        """
        execute method will result in execution of component body. Result depends on the component type. 
        A web application can generate HTML content where a graph based component gets all of inputs and 
        generate outputs. execute is the basic behaviour of the component on execution time. The application 
        is expected to call execute method of all added components to execute a design.
        """
        pass

    def resize(self, image):
        image.resize(self.__dict__['width'], self.__dict__['height'])


if __name__ == "__main__":
    resize = Resize()
    resize["width"] = 60
    resize["height"] = 60
    print resize["width"], resize["height"], resize.__dict__
