#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image


class Resize():
    """
    Resize image
    """
    def __init__(self):
        self.exec_image = None
        self.image_name = None

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
        dic = [('get_image_with_filename', 'This method gets image with the path and returns it. Provide path parameter as string')]
        dic = dic + [('get_image_with_url', 'This method gets image with the url and returns it. Provide url parameter as string')]
        dic = dic + [('get_image_width', 'This method returns the width of the image. Provide the image item you get with the path or url')]
        dic = dic + [('get_image_height', 'This method returns the height of the image. Provide the image item you get with the path or url')]
        dic = dic + [('resize_width', 'This method resizes the image width and it takes 3 parameters. As a first parameter provide the image you get with the path or url. As the second parameter provide the width you want to resize the image. As the last parameter provide the image name you want to save after image resize operation')]
        dic = dic + [('resize_height', 'This method resizes the image height and it takes 3 parameters. As a first parameter provide the image you get with the path or url. As the second parameter provide the height you want to resize the image. As the last parameter provide the image name you want to save image after resize operation')]
        dic = dic + [('resize_with_value', 'This method resizes the image width and height and it takes 4 parameters. As a first parameter provide the image you get with the path or url. As the second parameter provide the width you want to resize the image. As the third parameter provide the height you want to resize the image. As the last parameter provide the image name you want to save image after resize operation')]
        dic = dic + [('resize_with_ratio', 'This method resizes the image width and height and it takes 4 parameters. As a first parameter provide the image you get with the path or url. As the second parameter provide a ratio as float to multiply with the width. As the third parameter provide a ratio as float to multiply with the height. As the last parameter provide the image name you want to save image after resize operation')]

        return dic


    def execute(self):
        self.exec_image.save(filename=self.image_name)
        """
        execute method will result in execution of component body. Result depends on the component type. 
        A web application can generate HTML content where a graph based component gets all of inputs and 
        generate outputs. execute is the basic behaviour of the component on execution time. The application 
        is expected to call execute method of all added components to execute a design.
        """
        pass

    def get_image_with_filename(self,path):
        ret_image = Image(filename = path)
        self.exec_image = ret_image
        return ret_image

    def get_image_with_url(self,url):
        ret_image = Image(filename = url)
        self.exec_image = ret_image
        return ret_image

    def get_image_width(self,image):
        return image.width

    def get_image_height(self,image):
        return image.height

    def resize_with_ratio(self,image,ratio,newName):
        image.resize(int(image.width*ratio),int(image.height*ratio))
        self.exec_image = image
        self.image_name = newName
        #image.save(filename=newName)
        return image

    def resize_with_value(self,image,w_value,h_value,newName):
        image.resize(int(w_value),int(h_value))
        #image.save(filename=newName)
        self.exec_image = image
        self.image_name = newName
        return image

    def resize_width(self,image,w_value,newName):
        image.resize(int(w_value),image.height)
        self.exec_image = image
        self.image_name = newName
        #image.save(filename=newName)
        return image
    
    def resize_height(self,image,h_value,newName):
        image.resize(image.width,int(h_value))
        self.exec_image = image
        self.image_name = newName
        #image.save(filename=newName)
        return image


if __name__ == "__main__":
    resize = Resize()
    m = resize.get_image_with_url('https://developers.google.com/webmasters/mobile-sites/imgs/mobile-seo/separate-urls.png?hl=tr')
    print resize.get_image_width(m)
    print resize.get_image_height(m)
    m = resize.resize_with_value(m,100,90,'second.png')
    print resize.get_image_width(m)
    print resize.get_image_height(m)
    m = resize.resize_with_ratio(m,0.5,'second.png')
    print resize.get_image_width(m)
    print resize.get_image_height(m)
    resize.execute()