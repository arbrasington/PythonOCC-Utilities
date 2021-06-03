from typing import *

from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepClass import BRepClass_FClassifier, BRepClass_FaceExplorer
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCC.Core.GeomAdaptor import GeomAdaptor_Surface
from OCC.Core.TopAbs import TopAbs_ON, TopAbs_IN
from OCC.Core.TopoDS import TopoDS_Shell
from OCC.Core.gp import gp_Pnt, gp_Pnt2d
from OCC.Extend.TopologyUtils import TopologyExplorer


def putPoint(point: gp_Pnt, surface: TopoDS_Shell, maxDistance: int = 10) -> \
        Union[gp_Pnt, Tuple[None, None]]:
    """
    * This function places a point onto the geometry

    :param point: Point being placed
    :param surface: Surface that point is placed on
    :param maxDistance: Maximum allowable distance between projection and surface

    :return result: either the point of a tuple of (None, None) if failed
    TODO: Add reasoning for 'maxDistance = 10'
    """
    print('Dropping point:', point.Coord())

    for face in TopologyExplorer(surface).faces():  # try dropping point on each face
        sf = BRep_Tool.Surface(face)  # face to BRep

        geomAdaptor = GeomAdaptor_Surface(sf)  # convert to geometry surface
        a = GeomAPI_ProjectPointOnSurf(point, sf)  # project 3d pnt onto brep surface
        u, v = a.LowerDistanceParameters()
        pnt2d = gp_Pnt2d(u, v)

        evalPnt = geomAdaptor.Value(u, v)

        dist = evalPnt.Distance(point)
        if dist > maxDistance:
            continue

        result = BRepClass_FClassifier(BRepClass_FaceExplorer(face), pnt2d, 10 ** -3).State()  # test result
        print('Adaptor result:', result)
        if result == TopAbs_ON or result == TopAbs_IN:  # in boundary regions if 0
            # if a.NbPoints() > 2: continue  # this can be used to eliminate errors sometimes

            return a.Point(1)  # returns the first point that was found

    return None, None
