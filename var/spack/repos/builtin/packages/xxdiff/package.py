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
import inspect


class Xxdiff(MakefilePackage):
    """Graphical File And Directories Comparator And Merge Tool."""

    homepage = "http://furius.ca/xxdiff/"
    url      = "https://downloads.sourceforge.net/project/xxdiff/xxdiff/4.0.1/xxdiff-4.0.1.tar.bz2"

    version('4.0.1', '34253b829e249faf2480a989487e99bc')

    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))
    depends_on('qt@4.5:4.99')
    depends_on('flex', type='build')
    depends_on('bison', type='build')

    def build(self, spec, prefix):
        with working_dir('src'):
            make = inspect.getmodule(self).make
            make('-f', 'Makefile.bootstrap',
                 'QMAKE=%s' % join_path(spec['qt'].prefix.bin, 'qmake'))
            make()

    def install(self, spec, prefix):
        mkdirp(spec.prefix.bin)
        with working_dir('bin'):
            install('xxdiff', spec.prefix.bin)
