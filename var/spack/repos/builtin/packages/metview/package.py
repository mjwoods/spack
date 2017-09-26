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


class Metview(CMakePackage):
    """Metview is a meteorological workstation application designed to be a
    complete working environment for both the operational and research
    meteorologist. Its capabilities include powerful data access, processing
    and visualisation."""

    homepage = "https://software.ecmwf.int/wiki/display/METV/Metview"
    url      = "https://software.ecmwf.int/wiki/download/attachments/3964985/Metview-4.8.4-Source.tar.gz?api=v2"

    version('4.8.7', 'd7ee921bd40ce8971000be95101a5b8c102082cd')
    version('4.8.4', '0a07273ffdae3b6dddbe40f06723ea8a')

    variant('gui', default=True, description='Enable Qt-based user interface')
    variant('magics', default=True, description='Enable plotting capabilities using Magics')
    variant('proj', default=False, description='Enable support for OPERA radar data')
    variant('odb', default=False, description='Enable processing and plotting of ODB data')
    variant('eccodes', default=False, description='Use ecCodes (True) or GRIB-API (False) for GRIB handling')

    def chkmars(value):
        """Existing directory or '' to disable."""
        return value == '' or os.path.isdir(value)
    variant('mars', default='', values=chkmars, 
            description='Specify directory of external Mars client software')

    depends_on('qt@4.6.2:', when='+gui')
    depends_on('image-magick', when='+gui')
    depends_on('proj', when='+proj')

    depends_on('magics+netcdf+metview+qt~eccodes', when='+magics+gui~eccodes')
    depends_on('magics+netcdf+metview~qt~eccodes', when='+magics~gui~eccodes')
    depends_on('magics+netcdf+metview+qt+eccodes@2.29.1:', when='+magics+gui+eccodes')
    depends_on('magics+netcdf+metview~qt+eccodes@2.29.1:', when='+magics~gui+eccodes')
    depends_on('libemos~eccodes', when='~eccodes')
    depends_on('libemos+eccodes', when='+eccodes')
    depends_on('eccodes', when='+eccodes')
    depends_on('grib-api', when='~eccodes')
    depends_on('odb-api+eccodes', when='+odb+eccodes')
    depends_on('odb-api~eccodes', when='+odb~eccodes')
    
    #depends_on('gdbm')
    depends_on('netcdf')
    depends_on('curl')
    depends_on('bison')
    depends_on('flex+lex')
    depends_on('perl')
    depends_on('perl-xml-parser')

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
        if self.spec.variants['mars'].value == '':
            args.append('-DENABLE_MARS=OFF')
        else:
            args.append('-DENABLE_MARS=ON')
            args.append('-DMARS_LOCAL_HOME=' + self.spec.variants['mars'].value)
        if self.spec.satisfies('+odb'):
            args.append('-DENABLE_ODB=ON')
            args.append('-DODB_API_PATH=%s' % self.spec['odb-api'].prefix)
        else:
            args.append('-DENABLE_ODB=OFF')
        args.append('-DENABLE_MARS_ODB=OFF')
        args.append('-DNETCDF_PATH=%s' % self.spec['netcdf'].prefix)
        args.append('-DEMOS_PATH=%s' % self.spec['libemos'].prefix)
        return args

