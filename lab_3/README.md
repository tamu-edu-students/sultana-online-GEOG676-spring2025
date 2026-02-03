\# create classes

class Shape():

    def \_\_init\_\_(self):

        pass





class Rectangle(Shape):

    def \_\_init\_\_(self, l, w):

        self.length = l

        self.width = w

    def getArea(self):

        return self.length \* self.width



class Circle(Shape):

    def \_\_init\_\_(self, r):

        self.radius = r

    def getArea(self):

        return 3.14 \* self.radius \* self.radius



class Triangle(Shape):

    def \_\_init\_\_(self, b, h):

        self.base = b

        self.height = h

    def getArea(self):

        return 0.5 \* self.base \* self.height



\# read txt file

file = open(r'D:\\GEOG676\\New\_folder\\shape.txt', 'r')

lines = file.readlines()

file.close()



for line in lines:

    components = line.split(',')

    shape = components\[0]



    if shape == 'Rectangle':

        rect = Rectangle(int(components\[1]), int(components\[2]))

        print('Area of Rectangle is: ', rect.getArea())

    elif shape == 'Circle':

        cirl = Circle(int(components\[1]))

        print('Area of Circle is: ', cirl.getArea())

    elif shape == 'Triangle':

        tri = Triangle(int(components\[1]), int(components\[2]))

        print('Area of Triangle is: ', tri.getArea())

    else:

        pass

