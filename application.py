#!/usr/bin/env python
# -*- coding: utf-8 -*-
import components
import os
import imp
import inspect
import json

import design


class Application:

    def __init__(self):
        self.loaded_component = []
        self.design = design.Design()

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
        for i in self.loaded_component:
            d[i[0]] = i[3].description()
        return d

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
        cmps = []
        with open(path, 'r') as f:
            d = json.load(f)
            for x in d.cmps:
                # load component
                r = self.load(x.cmp)
                # create class instance
                cc = getattr(r[1], r[2])()
                # set args back
                for k, v in x.args.iteritems():
                    cc[k] = v
                # create entry
                de = design.DesignEntry(cc, x.cmp)
                # set saved id
                de.id = x.id
                # set method name
                de.method = x.method
                # add to list
                cmps.append(de)

        self.design.cmps = cmps

    def saveDesign(self, path):
        """
        A design can be saved and loaded from a file. The file format depends on you. Loading a design 
        should load() all required components and create all instances with their configured attributes.
        """
        self.design.save_to(path)

    def addInstance(self, componentname, index):
        """
        addInstance will create an instance from a loaded component and place it on given coordinates. The 
        coordinates can be on a grid, on a column or row layout. x and y parameters can be modified or new 
        parameters can be added as you need.
        addInstance should return a string id for the created component instance. Later calls will refer to 
        this id when they need to access the component.        
        """
        for x in self.loaded_component:
            if x[0] == componentname:
                cc = getattr(x[1], x[2])()
                # create entry
                de = design.DesignEntry(cc, componentname)
                de.index = index
                self.design.push(de)
                return de.index
        return None

    def instances(self):
        """
        instances return the current set of components in the application as a dictionary. The returned
         dictionary will have the component instance id as the key and component name and its position 
         in a tuple as the value.
        METU Department of Computer Engineering
        {’rss1231’:(’rss’,0,1), ’rss1212’:(’rss’,1,1), ’mb121’:(’mblog’,2,1)}.
        """
        index = -1
        r = {}
        for x in self.design.cmps:
            index += 1
            r[x.id] = (x.cmp_name, index)
        return r

    def removeInstance(self, id):
        """
        removeInstance will remove a component instance from the current design.
        """
        self.design.remove(id)


if __name__ == "__main__":
    app = Application()
    # print app.avaliable()
    app.avaliable()
    app.load('resize')
    app.loaded()
    a = app.addInstance('resize', 0)
    print app.addInstance('resize', 1)
    print app.instances()
    app.removeInstance(a)
