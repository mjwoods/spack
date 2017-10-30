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

    version('11689', revision='11689',
            svn='https://code.metoffice.gov.uk/svn/lfric/LFRic/trunk')
    version('trunk', svn='https://code.metoffice.gov.uk/svn/lfric/LFRic/trunk')
    version('dev', svn='https://code.metoffice.gov.uk/svn/lfric/LFRic/branches/dev/miltonwoods/r11763_fix_tests_gfortran_openmpi')

    depends_on('mpi')
    depends_on('netcdf+mpi')
    depends_on('netcdf-fortran')
    depends_on('netcdf-cxx')
    # lfric uses -lesmf, which does not reference all dependent libraries.
    # If we use default esmf variants, missing symbols occur.
    # So we keep the variants to a minimum here.
    # Or we could link with -lesmf_fullylinked to pull in dependent libs,
    # but that doesn't work for static builds.
    depends_on('esmf~xerces~pnetcdf~lapack')
    depends_on('xios')
    depends_on('pfunit+mpi+openmp')

    depends_on('gmake', type='build')
    depends_on('python', type='build')
    #depends_on('py-pyparsing', type='build')
    #depends_on('py-fparser', type='build')
    depends_on('py-jinja2', type='build')
    #depends_on('py-psyclone', type='build')
    depends_on('psyclone', type='build')
    depends_on('py-numpy', type='build')

    # Debug:
    parallel = False

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
        spack_env.set('LDMPI', self.spec['mpi'].mpifc)
        spack_env.set('PROFILE', 'fast-debug')
