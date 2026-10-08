import vtk

# 创建一个 DICOM 图像读取器
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName("D:\dicom文件\dcm\MR01010002.dcm")
reader.Update()

# 创建一个映射器
mapper = vtk.vtkImageMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# 创建一个演员
actor = vtk.vtkActor2D()
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