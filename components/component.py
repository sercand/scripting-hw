#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Component:
    """
    The Component interface
    """

    def description(self):
        """
        description returns a string describing what component does.
        """
        pass

    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are
         used at design time to configure a components behaviour.
        For example an RSS reader component may get the url of the RSS feed and number of most 
        recent messages to display as attributes. attributes should return [(’url’,’string’),(’msgcount’,’int’)].
        """
        pass
    
    def __setitem__(self, key, item):
        pass

    def __getitem__(self, key):
        pass

    def methods(self):
        """
        methods return a list of method calls and their descriptions. The methods define the behaviour of the 
        component at execution time. This way, application can interact with the components. RSS reader 
        can return [(’getpage’, ’Changes␣current␣page␣to␣given␣page␣no’)] so that user can go to arbitrary
        pages on reader. getpage() should be implemented on the RSS reader component
        class.
        """
        pass
