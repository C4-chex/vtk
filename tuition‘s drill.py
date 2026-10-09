#目标
#鼠标点击打印坐标：用 vtkRenderWindowInteractor，监听 'LeftButtonPressEvent'，打印点击时的世界坐标。



#自定义交互：写一个 vtkInteractorStyle 子类，按键盘 'r' 键时重置相机。



# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderer, vtkRenderWindowInteractor, vtkWorldPointPicker
)




def main(argv):
    colors = vtkNamedColors()


    cone = vtkConeSource()
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(10)


    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())


    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(colors.GetColor3d("Brown"))


    ren1 = vtkRenderer()
    ren1.AddActor(coneActor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))
    ren1.ResetCamera()


    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(300, 300)
    renWin.SetWindowName('Tutorial_Step2')

    #接下来使用iren将交互器和renwin做绑定
    # iren
    #  └─→ renWin(通过SetRenderWindow绑定)
    #       └─→ ren1(通过renWin.AddRenderer绑定)
    #             └─→ camera(renderer自带的活动相机)



    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    C1 = Call4It(ren1)
    #先解释为什么要defCall4It
        #因为这下面的这个AddObserver的部分 要求传入的ev（回调）应该含有1，call属性 2，函数属性 3，vtkCommand子类【我现在也不知道是什么】三选一
        #所以这边直接传ren1之类的变量名是不行的 所以class一个含call的类
    #再解释Call4It的参数部分
        #要传什么？-------这个对象由ev触发时所处的场景决定
            #在本实例中 leftbuttonpressevent所处的场景是在renderer中

    #所以为了指代该renderer 这个地方有两种选择
        #1 传iren 因为iren持有renwin renwin持有ren1
        #2 传ren1（即renderer的直属id）     推荐！！！！！
                                            #因为在这个地方 能传iren是因为只有这一个renderer 而且传Iren反应更慢
    iren.AddObserver('LeftButtonPressEvent',C1)

    iren.Initialize()
    iren.Start()





class Call4It():
    def __init__(self, renderer):
        self.renderer = renderer

    def __call__(self,caller,ev):
        x,y = caller.GetEventPosition()#注意 这里拿的是屏幕坐标 所以下一步做 屏幕坐标 --》世界坐标的exchange
        picker = vtkWorldPointPicker() #创建世界坐标拾取器picker
        picker.Pick(x,y,0,self.renderer) #（x,y,z,被调用的拾取场景）
        print('世界坐标:', picker.GetPickPosition())





# class vtkMyCallback(object):
#
#     def __init__(self, renderer):
#         self.renderer = renderer
#
#     def __call__(self,caller,ev):
#         position = self.renderer.GetActiveCamera().Position
#         print('({:5.2f}, {:5.2f}, {:5.2f})'.format(*position))


if __name__ == '__main__':
    import sys

    main(sys.argv)
