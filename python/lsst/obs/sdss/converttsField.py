#
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import sys
import os
import pyfits
import numpy as num
import lsst.afw.image as afwImage
import lsst.daf.base as dafBase


def converttsField(infile, filt, exptime = 53.907456):
    ptr = pyfits.open(infile)
    if ptr[0].header['NFIELDS'] != 1:
        print "INVALID TSFIELD FILE"
        sys.exit(1)
    filts = ptr[0].header['FILTERS'].split()
    idx = filts.index(filt)

    mjdTaiStart = ptr[1].data.field('mjd')[0][idx]        # MJD(TAI) when row 0 was read
    gain = float(ptr[1].data.field('gain')[0][idx])  # comes out as numpy.float32
    aa = ptr[1].data.field('aa')[0][idx]         # f0 = 10**(-0.4*aa) counts/second
    aaErr = ptr[1].data.field('aaErr')[0][idx]

    # Conversions
    mjdTaiMid = mjdTaiStart + 0.5 * exptime / 3600 / 24
    fluxMag0 = 10**(-0.4 * aa) * exptime
    dfluxMag0 = fluxMag0 * 0.4 * num.log(10.0) * aaErr

    calib = afwImage.Calib()
    calib.setMidTime(dafBase.DateTime(mjdTaiMid))
    calib.setExptime(exptime)
    calib.setFluxMag0(fluxMag0, dfluxMag0)

    ptr.close()

    return calib, gain

if __name__ == '__main__':
    infile = sys.argv[1]
    filt = sys.argv[2]
    if not os.path.isfile(infile):
        sys.exit(1)

    converttsField(infile, filt)
