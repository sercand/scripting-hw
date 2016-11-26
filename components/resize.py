import component


class Resize(component.Component):

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
        pass

    def getitem(self):
        """
        Component attribute values should be set and get by square bracket selector. For example 
        rss[’url’]=’http://a.com.tr/rss’ should set the URL of the RSS reader component named rss.
        Setting and/or getting a non-existing attribute should raise an exception of your choice.
        """
        pass

    def setitem(self):
        """
        Component attribute values should be set and get by square bracket selector. For example 
        rss[’url’]=’http://a.com.tr/rss’ should set the URL of the RSS reader component named rss.
        Setting and/or getting a non-existing attribute should raise an exception of your choice.
        """
        pass

    def methods(self):
        """
        methods return a list of method calls and their descriptions. The methods define the behaviour of the 
        component at execution time. This way, application can interact with the components. RSS reader 
        can return [(’getpage’, ’Changes␣current␣page␣to␣given␣page␣no’)] so that user can go to arbitrary
        pages on reader. getpage() should be implemented on the RSS reader componentclass.
        """
        pass

    def execute(self):
        """
        execute method will result in execution of component body. Result depends on the component type. 
        A web application can generate HTML content where a graph based component gets all of inputs and 
        generate outputs. execute is the basic behaviour of the component on execution time. The application 
        is expected to call execute method of all added components to execute a design.
        """
        pass
