##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import inspect


class Lfric(MakefilePackage):
    """Successor to the Unified Model at the UK Met Office."""

    homepage = "https://code.metoffice.gov.uk/trac/lfric"
    url = "https://code.metoffice.gov.uk/trac/lfric/browser"

    version('11638', revision='11638',
            svn='https://code.metoffice.gov.uk/svn/lfric/LFRic/trunk')
    version('trunk', svn='https://code.metoffice.gov.uk/svn/lfric/LFRic/trunk')

    depends_on('mpi')
    depends_on('netcdf+mpi')
    depends_on('netcdf-fortran')
    depends_on('netcdf-cxx')
    depends_on('esmf~xerces')
    depends_on('xios')

    depends_on('gmake', type='build')
    depends_on('python', type='build')
    depends_on('py-pyparsing', type='build')
    depends_on('py-fparser', type='build')
    depends_on('py-jinja2', type='build')
    depends_on('py-psyclone', type='build')
    depends_on('pfunit', type='build')

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            inspect.getmodule(self).make('VERBOSE=1')

    def setup_environment(self, spack_env, run_env):
        if self.spec.satisfies('%gcc'):
            spack_env.set('FPP', 'cpp -traditional-cpp')
        elif self.spec.satisfies('%intel'):
            spack_env.set('FPP', 'fpp')
        else:
            spack_env.set('FPP', 'ftn -eP')
        spack_env.set('LDMPI', 'mpif90')
        spack_env.set('PROFILE', 'fast-debug')
