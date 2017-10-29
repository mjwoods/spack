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


class Psyclone(Package):
    """Code generation for the PSyKAl framework from the GungHo project,
       as used by the LFRic model at the UK Met Office."""

    homepage = "https://github.com/stfc/PSyclone"
    url      = "https://github.com/stfc/PSyclone/archive/1.4.1.tar.gz"

    version('1.4.1', '47726fa62ecdefb9fb93fb7138d6cdcc')

    depends_on('python', type=('build', 'run'))
    depends_on('py-pyparsing', type=('build', 'run'))
    depends_on('py-fparser', type=('build', 'run'))

    # Use type='test' when available:
    depends_on('py-numpy', type='build')
    depends_on('py-nose', type='build')
    depends_on('py-pytest', type='build')

    conflicts('py-psyclone')  

    patch('install_mkdir.patch')

    def install(self, spec, prefix):
        if spec.satisfies('@1.5.0:'):
            raise InstallError('Use py-psyclone package for versions 1.5.0 onwards')
        install = Executable(join_path('contributions', 'install'))
        install(spec.prefix)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_build(self):
         with working_dir('src'):
             Executable('nosetests')()

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path('PYTHONPATH', self.spec.prefix.psyclone)
        run_env.prepend_path('PYTHONPATH', self.spec.prefix.psyclone)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path('PYTHONPATH', self.spec.prefix.psyclone)
        run_env.prepend_path('PYTHONPATH', self.spec.prefix.psyclone)
