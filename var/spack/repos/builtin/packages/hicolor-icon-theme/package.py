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


class HicolorIconTheme(AutotoolsPackage):
    """Default fallback theme for the freedesktop icon theme specification."""

    homepage = "https://www.freedesktop.org/wiki/"
    url      = "https://icon-theme.freedesktop.org/releases/hicolor-icon-theme-0.15.tar.xz"

    version('0.15', '6aa2b3993a883d85017c7cc0cfc0fb73')

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for this package."""
        run_env.prepend_path('XDG_DATA_DIRS',
                             join_path(self.prefix, 'share'))
