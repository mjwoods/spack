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
import os
import inspect


class MesaDemos(AutotoolsPackage):
    """Mesa 3D graphics demos collection"""

    homepage = "https://cgit.freedesktop.org/mesa/demos/"
    url      = "https://anongit.freedesktop.org/git/mesa/demos.git"

    version('8.3.0', git='https://anongit.freedesktop.org/git/mesa/demos.git',
            tag='mesa-demos-8.3.0')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('pkg-config', type='build')
    depends_on('makedepend', type='build')

    depends_on('mesa')
    depends_on('mesa-glu')
    depends_on('mesa-glut')
    depends_on('glew')

    def autoreconf(self, spec, prefix):
        """Not needed usually, configure should be already there"""
        # If configure exists nothing needs to be done
        if os.path.exists(self.configure_abs_path):
            return
        with working_dir(self.configure_directory):
            pkg_m4 = join_path(spec['pkg-config'].prefix, 'share', 'aclocal')
            m = inspect.getmodule(self)
            # This part should be redundant in principle, but
            # won't hurt
            m.libtoolize()
            m.aclocal('-I', pkg_m4)
            # This line is what is needed most of the time
            # --install, --verbose, --force
            autoreconf_args = ['-ivf', '-I', pkg_m4]
            m.autoreconf(*autoreconf_args)
