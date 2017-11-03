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
from distutils.dir_util import copy_tree


class Lfric(MakefilePackage):
    """Successor to the Unified Model at the UK Met Office."""

    homepage = "https://code.metoffice.gov.uk/trac/lfric"
    url = "https://code.metoffice.gov.uk/trac/lfric/browser"

    version('11689', revision='11689',
            svn='https://code.metoffice.gov.uk/svn/lfric/LFRic/trunk')
    version('trunk', svn='https://code.metoffice.gov.uk/svn/lfric/LFRic/trunk')
    version('dev', svn='https://code.metoffice.gov.uk/svn/lfric/LFRic/branches/dev/miltonwoods/r11763_fix_tests_gfortran_openmpi')

    patch('external_libraries_stdc++.patch', when='%gcc')

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
    depends_on('py-psyclone', type='build')
    #depends_on('psyclone', type='build')
    depends_on('py-numpy', type='build')

    def build(self, spec, prefix):
        with working_dir('mesh_tools'):
            inspect.getmodule(self).make('build', 'verbose=1')
        with working_dir('gungho'):
            inspect.getmodule(self).make('build', 'verbose=1')

    def install(self, spec, prefix):
        copy_tree(join_path('mesh_tools', 'bin'), prefix.bin)
        copy_tree(join_path('gungho', 'bin'), prefix.bin)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        with working_dir(join_path('mesh_tools', 'example')):
           cubemesh = join_path(self.prefix.bin,
                                'cubedsphere_mesh_generator')
           Executable(cubemesh)('cubedsphere.nml')
           bipmesh = join_path(self.prefix.bin,
                               'biperiodic_mesh_generator')
           Executable(bipmesh)('biperiodic.nml')
           summary = join_path(self.prefix.bin,
                               'summarise_ugrid')
           Executable(summary)('mesh_C12.nc')
        with working_dir(join_path('gungho', 'example')):
           mpiexec = Executable('mpiexec')
           gungho = join_path(self.prefix.bin, 'gungho')
           env['OMP_NUM_THREADS'] = '1'
           # Total number of processors must be a multiple of 6
           # for a cubed-sphere domain:
           mpiexec('-n', '6', gungho, 'gungho_configuration.nml')

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        if spec.satisfies('%gcc'):
            spack_env.set('FPP', 'cpp -traditional-cpp')
        elif spec.satisfies('%intel'):
            spack_env.set('FPP', 'fpp')
        else:
            spack_env.set('FPP', 'ftn -eP')
        if spec.satisfies('^openmpi'):
            spack_env.set('OMPI_MCA_orte_execute_quiet', '1')
            spack_env.append_flags('FFLAGS', '-I%s' % spec['mpi'].prefix.lib)
        spack_env.set('LDMPI', spec['mpi'].mpifc)
        spack_env.set('PROFILE', 'fast-debug')
