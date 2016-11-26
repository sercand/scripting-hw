#!/usr/bin/env python
# -*- coding: utf-8 -*-
import components
import os
import imp
import inspect
import design
import json


class Application:

    def __init__(self):
        self.loaded_component = []

    def avaliable(self):
        """
        Lists the names of the available components. Application has a directory path containing 
        python module files for the components. available method return list of such components 
        at run-time. Components can be installed even after the application started.
        A sample output could be [’rss’,’mblog’] indicating rss .py and mblog.py exists in the component directory.
        """
        # todo load libraries inside components folder
        available_list = []
        for root, dirs, files in os.walk("components"):
            for file in files:
                if (file.endswith(".py") and file != "__init__.py" and file != "component.py"):
                    available_list.append(file[:-3])
        return available_list

    def loaded(self):
        """
        Returns a dictionary of the names and descriptions of the loaded components.
        A sample output could be {’rss’:’RSS␣reader’,’mblog’:’A␣tiny␣microblog’}. Application can add
        instances of loaded components.
        """
        d = {}
        d[self.loaded_component[0]] = self.loaded_component[3]
        print d

    def load(self, compid):
        """
        load() is similar to Python import however it searches the module in component path. It keeps
        track of the component loaded and the class implementing the component so that instances can be created.
        """
        themodule = imp.load_source(compid, "components/" + compid + ".py")
        className = None
        for xn, obj in inspect.getmembers(themodule):
            if inspect.isclass(obj):
                if str(obj).startswith(compid):
                    className = str(obj).split('.')[1]
        class_ = getattr(themodule, className)
        ret = (compid, themodule, className, class_())
        self.loaded_component.append(ret)
        return ret

    def callMethod(self, id, methodname, params):
        """
        This method is used by application to call methods of the component instances.
        callMethod(’rss1231’,’refresh’,None) will call refresh () of the identified RSS component.        
        """
        pass

    def execute(self):
        """
        This is the application execution mode. It will execute all added component
        instances and generate the collective result. In web project it can be the whole 
        HTML page. In graph based projects it is the graph traversal resulting in the whole application action.        
        """
        pass

    def loadDesign(self, path):
        """
        A design can be saved and loaded from a file. The file format depends on you. Loading a design 
        should load() all required components and create all instances with their configured attributes.
        """
        d = design.Design()
        with open(path, 'r') as f:
            ds = json.load(f)
            for x in ds.cmps:
                r = self.load(x.cmp)
                cc = r[3]()
                de = design.DesignEntry(cc, x.cmp)

#        for x in self.cmps:
#           cmps.append({"id": x.id,
#                         "cmp": x.cmp_name,
#                         "method": x.method,
#                         "args": x.component.__dict__})
#

    def saveDesign(self, path):
        """
        A design can be saved and loaded from a file. The file format depends on you. Loading a design 
        should load() all required components and create all instances with their configured attributes.
        """
        pass

    def addInstance(self):
        """
        addInstance will create an instance from a loaded component and place it on given coordinates. The 
        coordinates can be on a grid, on a column or row layout. x and y parameters can be modified or new 
        parameters can be added as you need.
        addInstance should return a string id for the created component instance. Later calls will refer to 
        this id when they need to access the component.        
        """
        pass

    def instances(self):
        """
        instances return the current set of components in the application as a dictionary. The returned
         dictionary will have the component instance id as the key and component name and its position 
         in a tuple as the value.
        METU Department of Computer Engineering
        {’rss1231’:(’rss’,0,1), ’rss1212’:(’rss’,1,1), ’mb121’:(’mblog’,2,1)}.
        """
        pass

    def removeInstance(self):
        """
        removeInstance will remove a component instance from the current design.
        """
        pass


if __name__ == "__main__":
    app = Application()
    # print app.avaliable()
    app.load('resize')
    # app.loaded()
