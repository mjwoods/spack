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
import os


class MetviewBundle(CMakePackage):
    """Metview is a meteorological workstation application designed to be a
    complete working environment for both the operational and research
    meteorologist. Its capabilities include powerful data access, processing
    and visualisation. This package builds metview and supporting libraries
    from ECMWF.
    """

    homepage = "https://software.ecmwf.int/wiki/display/METV/Metview"
    url      = "https://software.ecmwf.int/wiki/download/attachments/51731119/MetviewBundle-2017.07.1-Source.tar.gz"

    version('2017.07.1', '00e31aa44fa7c2d1e80b6d637445f97967c838db')

    def isstr(value):
        """Path string or '' for default."""
        if sys.version_info[0] < 3:
            result = isinstance(value, basestring)
        else:
            result = isinstance(value, str)
        return result

    variant('odb', default=True, description='Enable processing and plotting of ODB data')
    variant('eccodes', default=True, description='Use ecCodes (True) or GRIB-API (False) for GRIB handling')
    variant('mars_client', default='', values=isstr,
        description='Location of external Mars client software')

    depends_on('qt@4.6.2:')
    depends_on('image-magick')
    depends_on('proj')

    depends_on('gdbm')
    depends_on('netcdf')
    # Note: needs netcdf-cxx instead of netcdf-cxx4 (for now)
    depends_on('netcdf-cxx')
    depends_on('cairo')
    depends_on('pango')
    depends_on('expat')

    depends_on('fftw+float+double')
    depends_on('openjpeg')
    depends_on('libpng')
    depends_on('boost')
    depends_on('jasper')

    depends_on('curl')
    depends_on('bison')
    depends_on('flex+lex')

    depends_on('pkg-config', type='build')
    depends_on('python', type='build')

    depends_on('perl', type='build')
    depends_on('perl-xml-parser', type='build')

    def cmake_args(self):
        args = ['-DECBUILD_LOG_LEVEL=DEBUG']

        # Extended source may be needed for long directory names:
        if self.spec.satisfies('%gcc'):
            fflags = '-ffree-line-length-none -ffixed-line-length-none'
            args.append('-DCMAKE_Fortran_FLAGS=%s' % fflags)

        cpref = [self.spec['qt'].prefix]
        args.append('-DCMAKE_PREFIX_PATH=%s' % ':'.join(cpref))
        if self.spec.satisfies('^qt@5:'):
            args.append('-DENABLE_QT5=ON')

        args.append('-DNETCDF_PATH=%s' % ':'.join(
                    [self.spec['netcdf'].prefix,
                     self.spec['netcdf-cxx'].prefix]))

        if self.spec.satisfies('+eccodes'):
            args.append('-DENABLE_ECCODES=ON')
        else:
            args.append('-DENABLE_ECCODES=OFF')

        if self.spec.satisfies('+odb'):
            args.append('-DENABLE_ODB=ON')
        else:
            args.append('-DENABLE_ODB=OFF')

        if self.spec.variants['mars_client'].value != '':
            args.append('-DENABLE_MARS=ON')
            args.append('-DMARS_LOCAL_HOME=' + self.spec.variants['mars_client'].value)

        return args
