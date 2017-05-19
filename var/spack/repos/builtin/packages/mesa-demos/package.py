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


class MesaDemos(AutotoolsPackage):
    """Mesa 3D graphics demos collection"""

    homepage = "https://cgit.freedesktop.org/mesa/demos/"
    url      = "ftp://ftp.freedesktop.org/pub/mesa/demos/8.3.0/mesa-demos-8.3.0.tar.bz2"

    version('8.3.0', '628e75c23c17394f11a316c36f8e4164')

    depends_on('mesa')
    depends_on('mesa-glu')
    depends_on('mesa-glut')
    depends_on('glew')
