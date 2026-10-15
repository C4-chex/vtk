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
    vtkRenderer
)
def main(argv):

    colors = vtkNamedColors()

    source = vtkCubeSource()
    source.SetXLength(3)
    source.SetYLength(3)
    source.SetZLength(3)



    writer = vtkSTLWriter()
    writer.SetFileName("weiter.stl")
    writer.SetInputConnection(source.GetOutputPort())
    writer.Write()

    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(source.GetOutputPort())

    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(colors.GetColor3d('Bisque'))

    ren1 = vtkRenderer()
    ren1.AddActor(coneActor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(300, 300)


    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)



    iren.Initialize()
    iren.Start()



if __name__ == '__main__':
    import sys

    main(sys.argv)

