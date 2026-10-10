import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderer  )



def main(argv):
    colors = vtkNamedColors()

    cone = vtkConeSource()
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(10)

    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())

    #
    # 创建一个actor代表第一个cone。Actor的属性通过设定不同的表面属性来调整。默认地，一个actor通过GetProperty()方法改变属性来创建。
    #
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(0.2, 0.63, 0.79)
    coneActor.GetProperty().SetDiffuse(0.7)#漫反射系数
    coneActor.GetProperty().SetSpecular(0.4)#镜面反射系数
    coneActor.GetProperty().SetSpecularPower(20)#高光指数

    #
    # 创建一个属性并直接设置，分配到第二个actor中
    #
    property = vtkProperty()
    property.SetColor(colors.GetColor3d("Tomato"))
    property.SetDiffuse(0.7)
    property.SetSpecular(0.4)
    property.SetSpecularPower(20)

    #
    # 创建第二个actor和一个property。Property被直接设置并分配到第二个actor中。通过这种方式，一个单独的property可以被分享给多个actor。
    # 即多个acotr可以采用相同的属性配置。
    # 注意，我们使用和第一个actor相同的mapper。这个方式避免了重复的几何属性，这样可以节省很多内存（如果几何尺寸过大）。
    coneActor2 = vtkActor()
    coneActor2.SetMapper(coneMapper)
    coneActor2.GetProperty().SetColor(colors.GetColor3d("LightSeaGreen"))
    coneActor2.SetProperty(property)  # 通过这句话设定的color为tomato（红色），如果注释了property中的tomato，即为上句设定的lightseagreen
    coneActor2.SetPosition(0, 2, 0)  # 这里设定的是第二个actor在视窗中的位置，由于每个锥体底面半径为1，设定在(0,2,0)可以使两个锥体沿着y轴无缝排列
                                    #（x,y,z)即是参数含义

    ren1 = vtkRenderer()
    ren1.AddActor(coneActor)
    ren1.AddActor(coneActor2)
    ren1.SetBackground(colors.GetColor3d("CornflowerBlue"))

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(300, 300)
    renWin.SetWindowName("Tutorial_Step4")

    for i in range(0, 360):#（可以沿用tuition3中的设置 但是这里我懒得改了）
        renWin.Render()
        ren1.GetActiveCamera().Azimuth(1)


if __name__ == '__main__':
    import sys

    main(sys.argv)