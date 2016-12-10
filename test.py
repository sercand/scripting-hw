import application
import base64

app = application.Application()

app.load('resize')
app.load('fx')
print app.loaded()

idr = app.addInstance('resize', 0, 'resize_with_value')
idf = app.addInstance('fx', 1, 'gamma')

app.instance(idr)['width'] = 600
app.instance(idr)['height'] = 600
app.instance(idf)['adj'] = 0.6

app.execute('sample.jpg', 'sample3.jpg')



with open("yourfile.ext", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())