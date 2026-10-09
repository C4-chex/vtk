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
    vtkRenderer
)


def main(argv):
    colors = vtkNamedColors()

    #
    # 这个pipeline的创建已在 Tutorial_Step1中介绍.
    #
    cone = vtkConeSource()
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(10)

    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))

    ren1 = vtkRenderer()
    ren1.AddActor(coneActor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))
    ren1.ResetCamera()

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(300, 300)
    renWin.SetWindowName('Tutorial_Step2')

    # 我们在这里设置observer.
    mo1 = vtkMyCallback(ren1)
    ren1.AddObserver('StartEvent', mo1)  #将ren1挂到mo1上 同时监听StartEvent
                                         #这里建立的关系是mo1持有ren1 不是继承
    for i in range(0, 360):

        # 渲染图像.
        renWin.Render()


        # 旋转主动相机1°
        ren1.GetActiveCamera().Azimuth(1)
                #Azimuth（方位角）后接参数 度
                # 获得当前相机，将相机沿着以焦点为中心的view up vector(Y轴)向上旋转，
                # 注意view up vector是通过setviewup设置的，并不一定垂直于投影的方向，其结果是相机的水平旋转（绕着焦点）。


class vtkMyCallback(object):
    """
    交互的Callback
    """


    def __init__(self, renderer):
        self.renderer = renderer


    def __call__(self, caller, ev):
        position = self.renderer.GetActiveCamera().GetPosition()  # 相对于世界坐标系，将在相机部分进行介绍
        print('({:5.2f}, {:5.2f}, {:5.2f})'.format(*position))


if __name__ == '__main__':
    import sys

    main(sys.argv)