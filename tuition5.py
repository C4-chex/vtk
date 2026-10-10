import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
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
    renWin.SetWindowName('Tutorial_Step5')
    #
    # vtkRenderWindowInteractor类在vtkRenderWindow中观察events(比如键盘按键或者鼠标)
    # 这些events被译成VTK可以理解的事件调用中。然后这些VTK events的observers可以适当地进行处理
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    #
    # 默认地，vtkRenderWindowInteractor实例化一个vtkInteractorStyle实例。
    # vtkInteractorStyle将它观察到的一组events转换成与vtkRenerWindowInteractor关联的vtkRenderWindow里相机、actors和/或属性上的操作。
    # 这里我们特殊说明一个特殊的交互风格：vtkInteractorStyleTrackballCamera
    style = vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)
    #
    # 不像之前的脚本我们执行一些操作并退出，这里我们保留一个运行的事件循环。用户可以使用鼠标和键盘在屏幕中根据当前的交互风格执行操作。
    # 当用户按下e，默认情况下vtkRenderWindowInteractor会调用一个exitevent。该调用会被捕获并退出事件循环（循环由start()触发）。
    #
    iren.Initialize()
    iren.Start()
    #
    # 最终注意：回顾observers可以观察特殊events并且采取合适的action。
    # 在渲染窗口中按下u会使vtkRenderWindowInteractor调用一个userevent。
    # 这个可以被捕获以弹出一个GUI等等。查看 Tcl Cone5.tcl 例子有关如何工作。


if __name__ == '__main__':
    import sys

    main(sys.argv)