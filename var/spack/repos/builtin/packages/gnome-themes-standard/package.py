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


class GnomeThemesStandard(AutotoolsPackage):
    """Various components of the default GNOME theme"""

    homepage = "https://developer.gnome.org"
    url      = "https://ftp.gnome.org/pub/gnome/sources/gnome-themes-standard/3.22/gnome-themes-standard-3.22.3.tar.xz"
    list_url = "https://ftp.gnome.org/pub/gnome/sources/gnome-themes-standard/"
    list_depth = 2

    version('3.22.3', 'b51c362b157b6407303d44f93c31ee11')

    variant('X', default=True, description="Enable an X toolkit")

    depends_on('gtkplus~X', when='~X')
    depends_on('gtkplus+X', when='+X')
    depends_on('perl', type='build')
    depends_on('perl-xml-parser', type='build')
    depends_on('intltool', type='build')

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for this package."""
        run_env.prepend_path('XDG_DATA_DIRS',
                             join_path(self.prefix, 'share'))

    def configure_args(self):
        """List of arguments for configure script, excluding --prefix."""
        if self.spec['gtkplus'].satisfies('@3:'):
            args = ['--disable-gtk2-engine']
        else:
            args = ['--disable-gtk3-engine']
        return args
