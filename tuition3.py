import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderer,
    vtkRenderWindowInteractor
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
    coneActor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))

    #
    # 创建两个renderers并分配actors。一个renderer通过vtkRenderWindow渲染在一个视窗里。在这个例子里，我们添加相同的actor到两个不同renderers，添加不同的actors到不同的renderers里也是可行的。
    #
    ren1 = vtkRenderer()
    ren1.AddActor(coneActor)
    ren1.SetBackground(colors.GetColor3d('RoyalBlue'))
    # SetViewport设定视窗大小在窗口的相对位置。前两个参数为视窗左上角(x,y)相对位置，后两参数为视窗右下角(x,y)相对位置。
    ren1.SetViewport(0.0, 0.0, 0.5, 1.0)  # 即占据窗口的左半部分

    ren2 = vtkRenderer()
    ren2.AddActor(coneActor)
    ren2.SetBackground(colors.GetColor3d('DodgerBlue'))
    ren2.SetViewport(0.5, 0.0, 1.0, 1.0)  # 即占据窗口的右半部分

    #对于SetViewport的参数 （左下角x坐标，左下角y坐标，右上角x坐标，右上角坐标）
    #这里的坐标不是像素坐标 而是归一化坐标 只能取0-1之间的数 类似于权重



    #
    # 最终我们创建渲染窗口，用于显示在屏幕中。
    # 我们使用AddRenderer将我们的renderer放进渲染窗口。我们也设定尺寸为300*300像素。
    #
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.AddRenderer(ren2)
    renWin.SetSize(600, 300)
    renWin.SetWindowName('Tutorial_Step3')


    #以下部分做了修改 因为原tuition中的for循环不方便观看 也没有衔接好tuition2中的interactor



    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    def rotate_camera(caller, event):
        ren1.GetActiveCamera().Azimuth(1)
        ren2.GetActiveCamera().Azimuth(1)
        caller.GetRenderWindow().Render()

    iren.AddObserver('TimerEvent', rotate_camera)
    iren.Initialize()
    #注意 这个地方的initialize的时机
            #如果先initialize再create timer就会导致在create timer之前iren就被初始化了
        #所以在这里补充：initialize的时机
            #1，initialize的作用是将iren所指向的interactor真正绑定到对应的renderwindow
            #2，为什么不把timer放到initialize之前？
                #打个比方：AddObserver = 在公司制度写一条「张三负责接电话」
                        #Initialize = 给公司装上电话总机
                        #Start = 开门营业
                        #timer = 让电话隔一段时间坏一次
    iren.CreateRepeatingTimer(100) #参数为毫秒
    iren.Start()


if __name__ == '__main__':
    import sys

    main(sys.argv)