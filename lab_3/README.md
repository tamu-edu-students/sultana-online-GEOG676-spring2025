\#GIS\_Programming
#Lab\_3



\# create classes

class Shape():

&nbsp;   def \_\_init\_\_(self):

&nbsp;       pass





class Rectangle(Shape):

&nbsp;   def \_\_init\_\_(self, l, w):

&nbsp;       self.length = l

&nbsp;       self.width = w

&nbsp;   def getArea(self):

&nbsp;       return self.length \* self.width



class Circle(Shape):

&nbsp;   def \_\_init\_\_(self, r):

&nbsp;       self.radius = r

&nbsp;   def getArea(self):

&nbsp;       return 3.14 \* self.radius \* self.radius



class Triangle(Shape):

&nbsp;   def \_\_init\_\_(self, b, h):

&nbsp;       self.base = b

&nbsp;       self.height = h

&nbsp;   def getArea(self):

&nbsp;       return 0.5 \* self.base \* self.height



\# read txt file

file = open(r'D:\\GEOG676\\New\_folder\\shape.txt', 'r')

lines = file.readlines()

file.close()



for line in lines:

&nbsp;   components = line.split(',')

&nbsp;   shape = components\[0]



&nbsp;   if shape == 'Rectangle':

&nbsp;       rect = Rectangle(int(components\[1]), int(components\[2]))

&nbsp;       print('Area of Rectangle is: ', rect.getArea())

&nbsp;   elif shape == 'Circle':

&nbsp;       cirl = Circle(int(components\[1]))

&nbsp;       print('Area of Circle is: ', cirl.getArea())

&nbsp;   elif shape == 'Triangle':

&nbsp;       tri = Triangle(int(components\[1]), int(components\[2]))

&nbsp;       print('Area of Triangle is: ', tri.getArea())

&nbsp;   else:

&nbsp;       pass

