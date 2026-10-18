

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkIOGeometry import vtkSTLReader, vtkSTLWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer, vtkCamera
)
import sys
import pygame
from pathlib import Path

folder = Path(input('请输入文件夹路径：'))
liles = list(folder.glob('*.stl'))















    
# def get_program_parameters():
# #这个def的逻辑是 终端输入指令之后 启动python程序 再由argparse读取参数 最后运行程序


#     import argparse  # 允许在运行时更改程序参数

#     description = 'Read a .stl file.'#命名而已

#     parser = argparse.ArgumentParser(description=description)#argparse.ArgumentParser()创建一个解析器对象，description是对程序的描述
#     parser.add_argument('filename', help='stl file') #add_argument()方法用于向解析器添加参数，'filename'是参数名，help是对参数的描述
#     args = parser.parse_args() #其实我自己觉得写个input加reader就够了 反正输入有错的话也会报错的
#     return args.filename

pygame.init()
pygame.joystick.init()
#为什么这里不能用pygame.joystick.Joystick  -->没有初始化joystick
#而且 joystick.Joystick 是一个类 要通过joystick.init()完成实例化

is_running = True






if pygame.joystick.get_count() == 0:
    print("未检测到手柄")
    exit()
joy1 = pygame.joystick.Joystick(0)
colors = vtkNamedColors()

filename = get_program_parameters()

reader = vtkSTLReader()
reader.SetFileName(sys.argv[1])
reader.Update()



coneMapper = vtkPolyDataMapper()          #以下部分之所以是cone是因为我从别的文件copy来的 懒得打了
coneMapper.SetInputConnection(reader.GetOutputPort())

coneActor = vtkActor()
coneActor.SetMapper(coneMapper)
coneActor.GetProperty().SetColor(colors.GetColor3d('Bisque'))



camera = vtkCamera()



ren1 = vtkRenderer()
ren1.AddActor(coneActor)
ren1.SetBackground(colors.GetColor3d('MidnightBlue'))


renWin = vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(300, 300)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren1.SetActiveCamera(camera)  # 从一开始就使用这台 Camera！！！！！！！！！！！！！！！！！！
ren1.ResetCamera()           # 根据模型范围调整位置、焦点和距离!!!!!!!!!!!!!!!!!!!!


def end(obj, event):
    global is_running
    is_running = False
    print('end')


iren.AddObserver("ExitEvent", end)      #（iren, "ExitEvent", end） 这个函数的意思是 当iren发生ExitEvent事件时 执行end函数

iren.Initialize()  #交互器初始化



def mode1():
    coneActor.SetOrigin(0, 0, 0)  
                    
    (a, b, c) = coneActor.GetPosition()
    
    if event.type == pygame.JOYAXISMOTION:
        if event.axis == 0  :
            coneActor.RotateZ(-rx)      #加上负号是因为手柄的轴值是正负的 但是旋转方向是相反的 所以要加负号
        elif event.axis == 1 :
            coneActor.RotateX(-ry)
        elif event.axis == 2:
            camera.Dolly(1.01**vb)
        elif event.axis == 3:
            camera.Dolly(1.01**vs)           #Dolly()方法是相机的缩放方法，参数是缩放倍数，1.01**vb表示根据手柄的轴值进行缩放
    camera.OrthogonalizeViewUp()            #因为在旋转过程中，摄像机的上方向可能会发生倾斜，所以需要重新正交化摄像机的上方向，以确保摄像机的视角保持正确
    ren1.ResetCameraClippingRange()        #修正摄像机的裁剪范围，以确保模型在视野内正确显示，避免被裁剪掉
    if current_mode == 2:
        mode2()

def mode2():
    center = reader.GetOutput().GetCenter()
    coneActor.SetOrigin(center)
    
    
    if event.type == pygame.JOYAXISMOTION:
        if event.axis == 0  :
            coneActor.RotateZ(-rx)
        elif event.axis == 1 :
            coneActor.RotateX(-ry)
        elif event.axis == 2:
            camera.Dolly(1.01**vb)
        elif event.axis == 3:
            camera.Dolly(1.01**vs)
    camera.OrthogonalizeViewUp()
    ren1.ResetCameraClippingRange()
    if current_mode == 1:
        mode1()      


current_mode = 0

clock = pygame.time.Clock()   #创建一个时钟对象，用于控制游戏循环的帧率

while is_running == True:

    iren.ProcessEvents()

    if not is_running:
        break



    for event in pygame.event.get():
        rx = joy1.get_axis(0)
        ry = joy1.get_axis(1)               
        vb = joy1.get_axis(2)
        vs = joy1.get_axis(3)
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                current_mode = 1
            if event.button == 1:
                current_mode = 2

    
        
        
        if event.type == pygame.QUIT:
            is_running = False
            break                                       #is_running = False 和 iren.TerminateApp() 不能同时使用 否则会报错
                                                        
        if is_running == False:
            iren.TerminateApp()                         #关闭程序怎么使用和挑选
            pygame.quit()
            break     

        if current_mode == 1:
            mode1()
        if current_mode == 2:
            mode2()
    renWin.Render()
    clock.tick(60)            #设置帧率
iren.TerminateApp()
renWin.Finalize()
pygame.quit()       
        
        
#总结关闭程序
        # break只退出最内层循环 比如在while-for结构中 for的break不会break while循环
        # iren.TerminateApp() 关闭vtk窗口但是不会跳出while循环
        # renWin.Finalize() 结束renwin的渲染 但是不会关闭别的东西
        # pygame.quit() 关闭pygame模块 但是不会结束python程序
        



# python vtk+stl+pygame.py Segmentation_1.stl


   
       
        
        
        
        



















