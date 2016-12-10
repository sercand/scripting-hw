import imp
import sys
import inspect

def load(name):
    themodule = imp.load_source(name, "components/" + name + ".py")
    className = None
    for xn, obj in inspect.getmembers(themodule):
        if inspect.isclass(obj):
            if str(obj).startswith(name):
                className = str(obj).split('.')[1]
    class_ = getattr(themodule, className)
    print themodule, className
    print class_
    return class_()


k = load("resize")
print k.description(), k.attributes()
