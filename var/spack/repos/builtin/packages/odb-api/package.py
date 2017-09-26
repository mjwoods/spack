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


class OdbApi(CMakePackage):
    """ODB API is a software developed at ECMWF for encoding and processing of observational data."""

    homepage = "https://software.ecmwf.int/wiki/display/ODBAPI/ODB+API+Home"
    url      = "https://software.ecmwf.int/wiki/download/attachments/61117379/odb_api_bundle-0.17.1-Source.tar.gz?api=v2"

    version('0.17.1', '37b4480873c10765a8896c4de9390afe')

    variant('eccodes', default=False, description='Use ecCodes (True) or GRIB-API (False) for GRIB handling')
    variant('odb', default=True, description='Support legacy ODB format')

    depends_on('doxygen', type='build')
    depends_on('perl', type='build')
    depends_on('pkg-config', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('lapack')
    depends_on('openssl')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('zlib')
    depends_on('netcdf')
    depends_on('boost')
    depends_on('eccodes', when='+eccodes')
    depends_on('grib-api', when='~eccodes')
    extends('python')

    def cmake_args(self):
        args = ['-DENABLE_FORTRAN=ON']
        if self.spec.satisfies('+odb'):
            args.extend(['-DENABLE_ODB=ON', '-DENABLE_MIGRATOR=ON'])
        else:
            args.extend(['-DENABLE_ODB=OFF', '-DENABLE_MIGRATOR=OFF'])
        if self.spec.satisfies('+eccodes'):
            args.append('-DENABLE_ECCODES=ON')
            args.append('-DECCODES_PATH=%s' % self.spec['eccodes'].prefix)
        else:
            args.append('-DENABLE_ECCODES=OFF')
            args.append('-DGRIB_API_PATH=%s' % self.spec['grib-api'].prefix)
        return args
