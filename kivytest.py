from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.clock import Clock

import math

class MyWidget(Widget):

    points = [[200,200],[200,300],[300,300],[300,200],[200,200]]
    affine = [[1,0,0],[0,1,0],[50,50,1]]
    count = 0;
    orig = [0,0]

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()

        Clock.schedule_interval(self.rotcall, 0.02)

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.5, 0.5, 0.5, 0.5)

            xarr = self.affine[0]
            yarr = self.affine[1]
            t = self.affine[2]

            xp = [xarr[0]*p[0] + yarr[0]*p[1] + t[0] + self.orig[0] for p in self.points]
            yp = [xarr[1]*p[0] + yarr[1]*p[1] + t[1] + self.orig[1] for p in self.points]    

            points_to_draw = [[xp[i],yp[i]] for i in range(len(self.points))]
            self.count += 1;
            print self.count, self.affine
            Line(points=tuple([i for a in points_to_draw for i in a]))
            Color(0.9, 0.9, 0.9, 1)
            Line(points=tuple([i for a in self.points for i in a]))

    def apply_to_affine(self, mat):
       
        self.affine = [[sum([self.affine[i][k]*mat[k][j] for k in range(3)])  for j in range(3)] for i in range(3)]

    def rotate(self, deg):
        cosr = math.cos(deg*math.pi/180)
        sinr = math.sin(deg*math.pi/180)
        self.apply_to_affine(([cosr, sinr, 0],[-sinr, cosr, 0],[0,0,1]))

    def translate(self, tx, ty):
        self.apply_to_affine([[1,0,0],[0, 1, 0],[tx, ty, 1]])

    def scale(self, s):
        self.apply_to_affine([[s,0,0],[0,s,0],[0,0,1]])

    def translate_orig(self, tx, ty):
        self.orig[0] = tx
        self.orig[1] = ty

    def rotcall(self, dt):
        self.translate(-250-self.orig[0],-250-self.orig[1])
        self.rotate(5)
        self.translate(250+self.orig[0],250+self.orig[1])
#        self.apply_to_affine([[1,0,0],[0, 1, 0],[-250, -250, 1]])
#        self.apply_to_affine([[0.984807753,0.173648178,0],[-0.173648178, 0.984807753, 0],[0, 0, 1]])
#        self.apply_to_affine([[1,0,0],[0, 1, 0],[250, 250, 1]])
#        self.translate_orig(50*math.cos(self.count*0.1),50*math.sin(self.count*0.1))
        self.translate(-200-self.orig[0],-200-self.orig[1])
        self.rotate(3)
        self.translate(200+self.orig[0],200+self.orig[1])
        self.update_canvas()

class MyApp(App):
    def build(self):
        return MyWidget()


MyApp().run()
