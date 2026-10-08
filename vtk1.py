
import vtk

# 创建一个立方体源
cube = vtk.vtkCubeSource()
cube.SetXLength(1.0)
cube.SetYLength(1.0)
cube.SetZLength(1.0)
cube.Update()

# 创建一个映射器
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(cube.GetOutputPort())

# 创建一个演员
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# 创建一个渲染器
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.3)

# 创建一个渲染窗口
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# 创建一个交互器
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# 启动交互
render_window.Render()
interactor.Start()