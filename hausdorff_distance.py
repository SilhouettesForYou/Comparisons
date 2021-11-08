import numpy as np
import vtk


def compute_distance(A, B):
    dist = []
    m = A.shape[0]
    n = B.shape[0]
    dim = A.shape[-1]
    for k in range(m):
        C = np.dot(np.ones([n, 1]),np.array(A[k]).reshape(1, dim))
        D = (C - B) * (C - B)
        D = np.sqrt(np.dot(D, np.ones([dim, 1])))
        dist.append(np.min(D))
    return np.max(dist)


def hausdorff_distance(A, B):
    """
    Hausdorff Distance: Compute the Hausdorff distance between two point clouds.
    Let A and B be subsets of a metric space (Z,dZ), 
    The Hausdorff distance between A and B, denoted by dH (A, B), is defined by:
    dH (A, B)=max{sup dz(a,B), sup dz(b,A)}, for all a in A, b in B,
    dH(A, B) = max(h(A, B),h(B, A)),  
    where h(A, B) = max(min(d(a, b))),  
    and d(a, b) is a L2 norm. 
    dist_H = hausdorff( A, B ) 
    A: First point sets. 
    B: Second point sets. 
    ** A and B may have different number of rows, but must have the same number of columns. ** 
    """
    return max(compute_distance(A, B), compute_distance(B, A))


def load_points(data):
    """
    :type data: vtk.data
    :rtype: np.darray
    """
    X = []
    points = data.GetPoints()
    for i in range(points.GetNumberOfPoints()):
        X.append(points.GetPoint(i))
    return np.array(X)

def load_data(filename):
    """
    :type filename: str
    :rtype: vtk.data
    """
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    reader.Update()
    
    return reader.GetOutput()

def load_datas(file_dir):
    """
    :type file dir: str e.g. "./datas/"
    :rtype: vtk.data
    """
    datas = []
    for file in os.listdir(file_dir):
        if file.endswith('.stl'):
            datas.append(load_data(file_dir + file))

    return datas

if __name__ == "__main__":
    A = load_points(load_data('./1-1-a.stl'))
    B = load_points(load_data('./1-2-a.stl'))
    dh = hausdorff_distance(A, B)
    print(dh)