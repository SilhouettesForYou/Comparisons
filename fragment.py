import vtk
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class Fragment:
    def __init__(self):
        self.id = None
        self.filename = ""
        self.fractures = []
        self.fragment = None
        self.cell_data = None
        self.point_data = None
        self.points = None
        self.COLOR = [
            [ 236, 247, 82 ],
            [ 121, 232, 208 ],
            [ 255, 184, 184 ],
            [ 134, 230, 90 ],
            [ 36, 209, 151 ],
            [ 150, 184, 255 ],
            [ 216, 99, 242 ],
            [ 255, 241, 153 ],
            [ 173, 255, 153 ],
            [ 255, 148, 148 ]
        ]


    def set_data(self, filename):
        """
        set the fragment data throungh filename
        :param filename: string type e.g. './plates/plate-4/fragment-1.stl'
        """
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)
        reader.Update()
        
        self.fragment = reader.GetOutput()
        self.cell_data = self.fragment.GetCellData()
        self.point_data = self.fragment.GetPointData()
        self.points = self.fragment.GetPoints()


    def point_to_array(self, point):
        """
        Convert point(vtk type) to array(np.darray type)
        :param point: vtk.vtkPoint type
        :return: a point with np.array type
        """
        return np.array([point[x] for x in range(3)])


    def get_curvatures(self, curvature_type='mean'):
        """
        compute curvature of fragment
        :param curvature_type: string type e.g. 'mean'
        :return: curvatures with type of dict
        """
        if self.fragment is None:
            return None
        curvatures = {}
        curvatures_filter = vtk.vtkCurvatures()
        curvatures_filter.SetInputData(self.fragment)
        if curvature_type == "mean":
            curvatures_filter.SetCurvatureTypeToMean()
        elif curvature_type == "min":
            curvatures_filter.SetCurvatureTypeToMinimum()
        elif curvature_type == "max":
            curvatures_filter.SetCurvatureTypeToMaximum()
        elif curvature_type == "Gaussian":
            curvatures_filter.SetCurvatureTypeToGaussian()
        curvatures_filter.Update()
        _curvatures = curvatures_filter.GetOutput().GetPointData().GetAttribute(0)
        for i in range(_curvatures.GetNumberOfTuples()):
            curvatures[i] = _curvatures.GetTuple(i)[0]
        return curvatures


    def set_color(self, colors, type='point'):
        """
        set color for fragment to renderer
        :param colors: vtk.vtkUnsignedCharArray type
        :param type: string e.g. 'point' or 'cell'
        :return: None
        """
        if self.fragment is None:
            return
        if type == 'cell' and colors.GetNumberOfTuples() is not self.fragment.GetNumberOfCells():
            return
        elif type == 'point' and colors.GetNumberOfTuples() is not self.fragment.GetNumberOfPoints():
            return
        
        if type == 'cell':
            self.fragment.GetCellData().SetScalar(colors)
        elif type == 'point':
            self.fragment.GetPointData().SetScalar(colors)

    
    def generate_points_from_threshold_curvature(self, curvatures, threshold_type='value', value=0):
        """
        genenrate points from filter curvatures by threshold
        :param curvatures: list type
        :param threshold_type string e.g. 'value' & the value int e.g. 0.2
        :return: filtered point(np.darray) and colors(vtk.vtkUnsignedCharArray)
        """
        if self.fragment is None:
            return
        points = []
        threshold = 0
        if threshold_type == 'value':
            threshold = value
        elif threshold_type == 'mean':
            threshold = np.mean(curvatures)
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        for i in range(len(curvatures)):
            rgb = [0, 0, 0]
            if curvatures[i] > threshold:
                points.append(self.point_to_array(self.points.GetPoint(i)))
                rgb = [self.COLOR[1][j] for j in range(3)]
            else:
                rgb = [self.COLOR[0][j] for j in range(3)]
            colors.InsertTuple3(i, *rgb)
        return np.array(points), colors


    def generate_points_data(self, points): 
        """
        genenrate points data from points(np.array)
        :param points: np.darray type
        :return: pooints(vtk.vtkPoints)
        """
        points_data = vtk.vtkPolyData()
        vertex_filter = vtk.vtkVertexGlyphFilter()
        
        if isinstance(points, np.ndarray):
            _points = vtk.vtkPoints()
            for point in points:
                _points.InsertNextPoint(point)
            points_data.SetPoints(_points)
        elif isinstance(points, vtk.vtkPoints):
            points_data.SetPoints(points)
        else:
            return None

        vertex_filter.SetInputData(points_data)
        vertex_filter.Update()

        return vertex_filter.GetOutput()


    def paint_points(self, X):
        """
        paint points with matplotlib
        :param X: np.array type
        :return: None
        """
        fig = plt.figure() 
        ax = Axes3D(fig)    
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], marker='o', s=50, c='blue')
        ax.set_xlabel('x', color='r')
        ax.set_ylabel('y', color='g')
        ax.set_zlabel('z', color='b') 


    def render_in_same_win(self, datas, **args):
        """
        render datas in the same window
        :param datas: list type
        :param **args some properties
        :return: None
        """
        renWin = vtk.vtkRenderWindow()
        ren= vtk.vtkRenderer()
        if datas is None:
            mapper = vtk.vtkPolyDataMapper()  
            mapper.SetInputData(self.fragment)  

            actor = vtk.vtkActor()  
            actor.SetMapper(mapper)
            if 'actor_color' in args and args['actor_color'] != 'None':
                actor.GetProperty().SetColor(np.array(self.COLOR[0]) / 255.0)
            if 'point_size' in args:
                actor.GetProperty().SetPointSize(int(args['point_size'])) 
            ren.AddActor(actor)
        else:
            for i in range(len(datas)):
                mapper = vtk.vtkPolyDataMapper()  
                mapper.SetInputData(datas[i])  
                
                actor = vtk.vtkActor()  
                actor.SetMapper(mapper) 

                if 'actor_color' in args:
                    if args['actor_color'] == 'index':
                        actor.GetProperty().SetColor(np.array(self.COLOR[i % len(self.COLOR)]) / 255.0)
                    elif len(args['actor_color']) is len(datas):
                        actor.GetProperty().SetColor(self.hex_to_rgb(args['actor_color'][i]) / 255.0)
                if 'point_size' in args:
                    actor.GetProperty().SetPointSize(int(args['point_size']))

                ren.AddActor(actor)  

        ren.SetBackground(0 / 255.0, 166 / 255.0, 222 / 255.0)
        renWin.AddRenderer(ren)
        renWin.Render()
        iren=vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)
        
        iren.Initialize()
        iren.Start()


    def hex_to_rgb(self, value):
        """
        convert hex to rgb
        :param value: string type
        :return: rgb(np.darray)
        """
        value = value.lstrip('#')
        lv = len(value)
        return np.array([int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)])
        
