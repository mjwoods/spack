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


class GnomeIconTheme(AutotoolsPackage):
    """Icons for GNOME and gtk applications"""

    homepage = "https://www.gnome-look.org"
    url      = "http://ftp.gnome.org/pub/gnome/sources/gnome-icon-theme/3.12/gnome-icon-theme-3.12.0.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/gnome-icon-theme/"
    list_depth = 2

    version('3.12.0', 'f14bed7f804e843189ffa7021141addd')

    variant('X', default=True, description="Enable an X toolkit")

    depends_on('hicolor-icon-theme')
    depends_on('icon-naming-utils')
    depends_on('gtkplus~X', when='~X')
    depends_on('gtkplus+X', when='+X')
    depends_on('perl-xml-parser', type='build')
    depends_on('intltool', type='build')

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for this package."""
        run_env.prepend_path('XDG_DATA_DIRS',
                             join_path(self.prefix, 'share'))
