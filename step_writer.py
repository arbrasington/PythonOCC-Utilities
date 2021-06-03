from pathlib import Path

from OCC.Core.IFSelect import IFSelect_RetError
from OCC.Core.Interface import *
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.STEPConstruct import stepconstruct_FindEntity
from OCC.Core.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCC.Core.TCollection import TCollection_HAsciiString
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.Transfer import Transfer_FinderProcess


class StepWriter(STEPControl_Writer):
    """
    * Contains functions that give ability to write to STEP files
    """

    def __init__(self, schema=3):
        """
        * Creates a Step Writer from scratch
        """
        super().__init__()
        assembly_mode = 2

        """
        1: ;AP214CD; (default): AP214, CD version (dated 26 November 1996),
        2: ;AP214DIS;: AP214, DIS version (dated 15 September 1998).
        3: ;AP203;: AP203, possibly with modular extensions (depending on data written to a file).
        4: AP214IS: AP214, IS version (dated 2002)
        """

        self.fp: Transfer_FinderProcess = self.WS().TransferWriter().FinderProcess()
        Interface_Static_SetIVal('write.step.schema', schema)
        Interface_Static_SetCVal('write.step.unit', 'MM')
        Interface_Static_SetIVal('write.step.assembly', assembly_mode)

    def writeNamedPart(self, shape: TopoDS_Shape, name: str):
        """
        * Translates shape to a STEP file and names it
        :param shape: Shape being translated
        :param name: Name of STEP file being created
        """
        Interface_Static_SetCVal('write.step.product.name', name)
        status = self.Transfer(shape, STEPControl_AsIs)
        if int(status) > int(IFSelect_RetError):
            raise Exception('Some Error occurred')

        # This portion is not working as I hoped
        item = stepconstruct_FindEntity(self.fp, shape)
        if not item:
            raise Exception('Item not found')

        item.SetName(TCollection_HAsciiString(name))

    def save(self, path: Path):
        """
        * Writes a STEP model in the file identified by filename.
        :param path: The location of the file within the directory
        """
        status = self.Write(str(path))
        if int(status) > int(IFSelect_RetError):
            raise Exception('Something bad happened')

    def Write(self, path: Path):
        """
        * Writes a STEP model in the file identified by filename.
        :param path: The location of the file within the directory
        """
        status = super().Write(str(path))
        if int(status) > int(IFSelect_RetError):
            raise Exception('Something bad happened')
