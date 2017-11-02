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

    version('0.0.5', 'e93d2eae721bf820cf60135473e9c5c7')

    depends_on('py-setuptools', type='build')

    depends_on('python', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))

    # Use type='test' when available:
    depends_on('py-nose', type='build')
    depends_on('py-py', type='build')
    depends_on('py-pytest', type='build')
    depends_on('py-six', type='build')
    depends_on('py-appdirs', type='build')
    depends_on('py-enum34', type='build')
    depends_on('py-hypothesis', type='build')
    depends_on('py-packaging', type='build')
    depends_on('py-pyparsing', type='build')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_build(self):
         # Ensure that pytest.ini exists inside the source tree,
         # otherwise an external pytest.ini can cause havoc:
         touch('pytest.ini')
         with working_dir('src'):
             Executable('py.test')()
