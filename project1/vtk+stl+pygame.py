

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


def get_program_parameters():
                                                    #这个def的逻辑是 终端输入指令之后 启动python程序 再由argparse读取参数 最后运行程序


    import argparse  # 允许在运行时更改程序参数

    description = 'Read a .stl file.'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('filename', help='stl file')
    args = parser.parse_args()
    return args.filename

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



def end(obj, event):
    global is_running
    is_running = False
    print('end')


iren.AddObserver("ExitEvent", end)

iren.Initialize()



def mode1():
    ren1.SetActiveCamera(camera)
                    
    (a, b, c) = coneActor.GetPosition()
    camera.SetPosition(a + 100, b + 100, c + 100)
    camera.SetFocalPoint(0, 0, 0)
    if event.type == pygame.JOYAXISMOTION:
        if event.axis == 0  :
            coneActor.RotateZ(5*rx)
        elif event.axis == 1 :
            coneActor.RotateX(5*ry)
        elif event.axis == 2:
            camera.Dolly(2*vb)
        elif event.axis == 3:
            camera.Dolly(2*vs)
    camera.OrthogonalizeViewUp()
    ren1.ResetCameraClippingRange()


def mode2():
    center = reader.GetOutput().GetCenter()
    coneActor.SetOrigin(center)
    iren.ProcessEvents()
    
    if event.type == pygame.JOYAXISMOTION:
        if event.axis == 0  :
            coneActor.RotateZ(5*rx)
        elif event.axis == 1 :
            coneActor.RotateX(5*ry)
        elif event.axis == 2:
            camera.Dolly(2*vb)
        elif event.axis == 3:
            camera.Dolly(2*vs)
    camera.OrthogonalizeViewUp()
    ren1.ResetCameraClippingRange()



current_mode = 0


while is_running == True:

    iren.ProcessEvents()

    for event in pygame.event.get():
        rx = joy1.get_axis(0)
        ry = joy1.get_axis(1)
        vb = joy1.get_axis(2)
        vs = joy1.get_axis(3)
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                current_mode = 1
            elif event.button == 1:
                current_mode = 2

    
        
        
        elif event.type == pygame.QUIT:
            is_running = False
            break

        elif is_running == False:
            iren.TerminateApp()
            pygame.quit()
            break     

    if current_mode == 1:
        mode1()
    elif current_mode == 2:
        mode2()
    renWin.Render()
        
        
        
        






# python mimi.py Segmentation_1.stl




   
       
        
        
        
        



















