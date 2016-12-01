import application

app = application.Application()

app.load('resize')
app.load('fx')
print app.loaded()

idr = app.addInstance('resize', 0, 'resize_with_value')
idf = app.addInstance('fx', 1, 'gamma')

app.callMethod(idr, 'set_image_width', 600)
app.callMethod(idr, 'set_image_height', 600)
app.callMethod(idf, 'set_gamma', 0.6)

app.execute('sample.jpg', 'sample3.jpg')

