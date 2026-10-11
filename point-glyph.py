#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkUnstructuredGrid
)
from vtkmodules.vtkFiltersCore import vtkAppendFilter
from vtkmodules.vtkFiltersSources import (
    vtkPointSource,
    vtkSphereSource
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    colors = vtkNamedColors()

    pointSource = vtkPointSource()      #这里的source是数据集                         vtkPointSource (数据源/算法)
                                                                                         #└── 输出 vtkPolyData (数据集)
                                                                                                      #└── 包含 vtkPoints (点容器)
                                                                                                                   #└── 包含具体的点坐标 (x,y,z)

    #设置5个point
    pointSource.SetNumberOfPoints(5)
    pointSource.Update()

    polydata = pointSource.GetOutput()

    # print('There are', polydata.GetNumberOfPoints(), 'points in the polydata.')
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^教程里面有的 但是我不想要


    #在vtkUnstructuredGrid中创建两个point
    points = vtkPoints()
    points.InsertNextPoint(0, 0, 0)    #世界坐标
    points.InsertNextPoint(0, 0, 1)


    ug = vtkUnstructuredGrid()#新建空网格
    ug.SetPoints(points) #把points绑定到ug中
    # print('There are', ug.GetNumberOfPoints(), 'points in the unstructured.')
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^教程里面有的 但是我不想要

    # Combine the two data sets
    appendFilter = vtkAppendFilter()
    appendFilter.AddInputData(polydata)                 #释疑（其实是我自己没搞懂）：这里为什么传source？
    appendFilter.AddInputData(ug)                       #因为AddInputData要的是数据类型参数 但是source属于算法
    appendFilter.Update()

    combined = vtkUnstructuredGrid()                    #这一行理论上没什么用 因为即使有这一行 也会被下一行get到的output覆盖
                                                        #但是这个是可能是为了vtk版本的api过渡 也可能是从cpp直译而来 我没学cpp我不知道

    combined = appendFilter.GetOutput()
    print('There are', combined.GetNumberOfPoints(), 'points combined.')

    #创建mapper和actor
    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(appendFilter.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(5)

    #把point渲染成spheres
    sphereActor = point_to_glyph(appendFilter.GetOutput().GetPoints(), 0.05)
    sphereActor.GetProperty().SetColor(colors.GetColor3d("Gold"))

    #创建renderer winrender interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    #将actor加入window
    renderer.AddActor(actor)
    renderer.AddActor(sphereActor)
    renderer.SetBackground(colors.GetColor3d('RoyalBlue'))

    # Render 和 interactor部分
    renderWindow.SetWindowName('AppendFilter')
    renderWindow.Render()   #渲染window
    renderWindowInteractor.Start()#启动交互器

    #sphereActor = point_to_glyph(appendFilter.GetOutput().GetPoints(), 0.05)
def point_to_glyph(points, scale):


    bounds = points.GetBounds()   #获取包围盒    bounds = (xmin, xmax, ymin, ymax, zmin, zmax)
                                  #这样就拿到了能包住所有点的一个立方体





    #——————————————————————————————————————————————————————————————————————————
    # for i in range(0, 3):
    #     max_len = max(bounds[i + 1] - bounds[i], max_len)
    #——————————————————————————————————————————————————————————————————————————
    #被包起来的这两行是官方教学里的 但是我不知道为什么这样写 因为目的是取xyz三维之间跨度最大的某个轴 所以我觉得可以这样写

    max_len = max(
        bounds[1]-bounds[0],
        bounds[3]-bounds[2],
        bounds[5]-bounds[4],
        )



    sphere_source = vtkSphereSource()   #生成球
    sphere_source.SetRadius(scale * max_len)    #设置半径

    pd = vtkPolyData()
    pd.SetPoints(points)            #这一步的作用是 把points是容器 但是 vtk的设计思想是只允许vtkDataObject（数据集）和他的子集贯穿管线
                                    #所以这里使用方法setpoints 把points塞进vtkPloyData（数据集的某个子集）中
                                    #Q: 那要怎么判断某个变量名是不是数据集呢
                                    #A：print(isinstance(变量名, vtk.vtkDataObject))


    mapper = vtkGlyph3DMapper()
    mapper.SetInputData(pd)
    mapper.SetSourceConnection(sphere_source.GetOutputPort())#不直接传sphere_source的原因是 connection要给端口 source是数据集


    mapper.ScalarVisibilityOff()   #上色用的
    mapper.ScalingOff()       #使大小相同
    #两个都是"关掉基于标量的自动行为",让结果显示更可控、更统一
    #也可以试试注释这两行看看结果
    # hh 其实没影响 因为上面根本没设置球的property



    actor = vtkActor()
    actor.SetMapper(mapper)

    return actor


if __name__ == '__main__':
    main()