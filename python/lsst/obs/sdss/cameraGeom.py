"""
Utilities to use SDSS data with the cameraGeom utilities.  For example:

import lsst.daf.persistence as dafPersist
import lsst.afw.cameraGeom.usils as cgUtils
import lsst.obs.sdss.makeCamera as makeCamera
from lsst.obs.sdss import SdssMapper;

butler = dafPersist.ButlerFactory(mapper=SdssMapper(root="/lsst7/stripe82/dr7/runs")).create()

camera = makeCamera.makeCamera()
cgUtils.showCamera(camera, imageSource=SdssCcdImage(butler=butler, run=94, frame=101), frame=1)

"""
import lsst.afw.geom as afwGeom
import lsst.afw.cameraGeom.utils as cgUtils

class SdssCcdImage(cgUtils.GetCcdImage):
    """A class to return an Image of a given SDSS Ccd by using the butler"""
    
    def __init__(self, butler, run, frame, *args):
        """Initialise"""
        super(SdssCcdImage, self).__init__(*args)
        self.butler = butler
        self.run = run
        self.frame = frame

    def getImage(self, ccd, amp=None, imageFactory=None):
        """Return the image of the chip with cameraGeom.Id == id; if provided only read the given amp"""

        band, camCol = list(ccd.getId().getName()) # list splits the name
        camCol = 3                                 # XXX
        fpC = self.butler.get("fpC", dict(run=self.run, camcol=camCol, band=band, frame=self.frame))

        if amp:
            if amp.getId().getSerial() == 0:
                origin = afwGeom.PointI(0, 0)
            else:
                origin = afwGeom.PointI(1024, 0)

            fpC = fpC.Factory(fpC, afwGeom.BoxI(origin, afwGeom.ExtentI(1024, 1361)))

        return fpC