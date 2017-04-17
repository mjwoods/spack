##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
from spack import *


class Metview(CMakePackage):
    """Metview is a meteorological workstation application designed to be a
    complete working environment for both the operational and research
    meteorologist. Its capabilities include powerful data access, processing
    and visualisation."""

    homepage = "https://software.ecmwf.int/wiki/display/METV/Metview"
    url      = "https://software.ecmwf.int/wiki/download/attachments/3964985/Metview-4.8.4-Source.tar.gz?api=v2"

    version('4.8.4', '0a07273ffdae3b6dddbe40f06723ea8a')

    variant('gui', default=True)
    variant('magics', default=True)
    variant('proj', default=False)
    variant('eccodes', default=False)

    depends_on('qt@4.6.2:', when='+gui')
    depends_on('image-magick', when='+gui')
    depends_on('proj', when='+proj')

    depends_on('magics+netcdf+metview+qt', when='+magics+gui')
    depends_on('magics+netcdf+metview', when='+magics~gui')
    depends_on('libemos')
    depends_on('eccodes', when='+eccodes')
    depends_on('grib-api', when='~eccodes')
    
    #depends_on('gdbm')
    depends_on('netcdf')
    depends_on('curl')
    depends_on('bison')
    depends_on('flex')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+gui'):
            args.append('-DENABLE_UI=ON')
            args.append('-DCMAKE_PREFIX_PATH=%s' % self.spec['qt'].prefix)
            if self.spec.satisfies('^qt@5:'):
                args.append('-DENABLE_QT5=ON')
        else:
            args.append('-DENABLE_UI=OFF')
        if self.spec.satisfies('+magics'):
            args.append('-DENABLE_PLOTTING=ON')
            args.append('-DMAGICS_PATH=%s' % self.spec['magics'].prefix)
        else:
            args.append('-DENABLE_PLOTTING=OFF')
        if self.spec.satisfies('+proj'):
            args.append('-DENABLE_OPERA_RADAR=ON')
            args.append('-DPROJ4_PATH=%s' % self.spec['proj'].prefix)
        else:
            args.append('-DENABLE_OPERA_RADAR=OFF')
        if self.spec.satisfies('+eccodes'):
            args.append('-DENABLE_ECCODES=ON')
            args.append('-DECCODES_PATH=%s' % self.spec['eccodes'].prefix)
        else:
            args.append('-DENABLE_ECCODES=OFF')
            args.append('-DGRIB_API_PATH=%s' % self.spec['grib-api'].prefix)
        args.append('-DENABLE_ODB=OFF')
        args.append('-DENABLE_MARS_ODB=OFF')
        args.append('-DNETCDF_PATH=%s' % self.spec['netcdf'].prefix)
        args.append('-DEMOS_PATH=%s' % self.spec['libemos'].prefix)
        return args

