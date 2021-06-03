import matplotlib.pyplot as plt
import numpy as np
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_CompCurve
from OCC.Core.TopoDS import TopoDS_Wire


def discretize_wire(wire: TopoDS_Wire, num=100):
    """
    Discretize a wire into an array of x,y,z coordinates.
    Array is in the format:
    [ [x1, y1, z2],
      [x2, y2, z2], ... ]

    Args:
        wire (TopoDS_Wire): wire to be discretized
        num (int): number of points to generate

    Returns:
        points (np.ndarray): array of x,y,z coordinates
    """
    if not isinstance(wire, TopoDS_Wire):
        raise Exception('Invalid input type, wire must be type: TopoDS_Wire')

    c = BRepAdaptor_CompCurve(wire)  # convert to geometry curve
    points = np.array([[c.Value(u).X(), c.Value(u).Y(), c.Value(u).Z()]
                       for u in np.linspace(c.FirstParameter(), c.LastParameter(), num)])

    return points
