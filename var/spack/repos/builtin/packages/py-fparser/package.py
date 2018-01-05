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


class PyFparser(PythonPackage):
    """Parser for Fortran 77..2003 code."""

    homepage = "https://github.com/stfc/fparser"
    url      = "https://github.com/stfc/fparser/archive/0.0.5.tar.gz"
    giturl   = "https://github.com/stfc/fparser.git"

    version('0.0.6', git=giturl,
            commit='638c51ec57cf17624505b70321c3784e356b8910')
    version('0.0.5', git=giturl,
            commit='a3ff86b635f7bd7bd281ee94cbd3d9455b288fd9')
    version('develop', git=giturl, branch='master')

    depends_on('py-setuptools', type='build')

    depends_on('py-numpy', type=('build', 'run'), when='@0:0.0.5')
    depends_on('py-nose', type='build')
    depends_on('py-six', type='build')

    # Use type='test' when available:
    depends_on('py-pytest', type='build')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        # Ensure that pytest.ini exists inside the source tree,
        # otherwise an external pytest.ini can cause havoc:
        touch('pytest.ini')
        with working_dir('src'):
            Executable('py.test')()
