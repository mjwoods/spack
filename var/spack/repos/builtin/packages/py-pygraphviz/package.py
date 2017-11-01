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


class PyPygraphviz(PythonPackage):
    """Interface to the Graphviz graph layout and visualization package."""

    homepage = "http://pygraphviz.github.io"
    url      = "https://pypi.io/packages/source/p/pygraphviz/pygraphviz-1.4rc1.tar.gz"

    version('1.4rc1', '2f950fb2a61a2dc85efc89543523ec07')

    depends_on('py-setuptools', type='build')
    depends_on('graphviz', type=('build', 'link', 'run'))

    phases = ['install']

    def install(self, spec, prefix):
        """Install everything from build directory."""
        args = self.install_args(spec, prefix)
        args.extend(['--include-path=%s' % spec['graphviz'].prefix.include,
                     '--library-path=%s' % spec['graphviz'].prefix.lib])
        self.setup_py('install', *args)