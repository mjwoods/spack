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


class Pfunit(CMakePackage):
    """pFUnit is a unit testing framework enabling JUnit-like testing of
    serial and MPI-parallel software written in Fortran."""

    homepage = "http://pfunit.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/pfunit/Source/pFUnit.tar.gz"

    version('3.2.8', commit='14339d668c3f7440c408422dea68d750ee59ad9d',
            git='https://git.code.sf.net/p/pfunit/code')
    version('master', branch='master',
            git='https://git.code.sf.net/p/pfunit/code')

    variant('mpi', default=True, description='Enable MPI')
    variant('openmp', default=True, description='Enable OpenMP')

    depends_on('python', type=('build','run'))
    depends_on('py-unittest2', type=('run'))
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = ['-DINSTALL_DIR=%s' % self.spec.prefix,
                '-DCMAKE_Fortran_MODULE_DIRECTORY=%s' % self.spec.prefix.include]
        if self.spec.satisfies('+mpi'):
            args.append('-DMPI=YES')
        else:
            args.append('-DMPI=NO')
        if self.spec.satisfies('+openmp'):
            args.append('-DOPENMP=YES')
        else:
            args.append('-DOPENMP=NO')
        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        if self.spec.satisfies('+mpi'):
            testdir = join_path('Examples', 'MPI_Halo')
        else:
            testdir = 'Examples'
        with working_dir(testdir):
            make('PFUNIT=%s' % self.spec.prefix)
