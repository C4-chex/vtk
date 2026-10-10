import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkBoxWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
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
    coneActor.GetProperty().SetColor(colors.GetColor3d('Bisque'))

    ren1 = vtkRenderer()
    ren1.AddActor(coneActor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(300, 300)
    renWin.SetWindowName('Tutorial_Step6')


    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)


    style = vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)


    # 这里我们使用 vtkBoxWidget 来变换底层的 coneActor
    # VTK 还提供了许多其他类型的 3D 控件,建议上官网查 https://examples.vtk.org/site/Python/Tutorial/Tutorial_Step6/


    boxWidget = vtkBoxWidget()#引入控件
    boxWidget.SetInteractor(iren)#绑定控件
    boxWidget.SetPlaceFactor(1.25)#参数是控件盒相对于物体的放大倍率
    boxWidget.GetOutlineProperty().SetColor(colors.GetColor3d('Gold'))
    #get out line property     获取轮廓的属性



    boxWidget.SetProp3D(coneActor) # 初始化控件位置。
    boxWidget.PlaceWidget()# 3D 控件以"输入的某个对象"作为参考,


    callback = vtkMyCallback()
    boxWidget.AddObserver('InteractionEvent', callback)



    boxWidget.On()# 通常情况下,用户需要按下 'i' 键才能激活 3D 控件。
    # 这里我们手动调用 On() 让它与圆锥一起显现。



    iren.Initialize()
    iren.Start()



class vtkMyCallback(object):



    def __call__(self, caller, ev):
        t = vtkTransform()
        widget = caller                 #这行写不写都行 但是解释一下 为什么widget是caller：
                                        #因为事件InteractionEvent被绑定在widget下
        widget.GetTransform(t)
        widget.GetProp3D().SetUserTransform(t)


if __name__ == '__main__':
    import sys

    main(sys.argv)
