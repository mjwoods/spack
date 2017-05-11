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
from spack import *


class Pcre(AutotoolsPackage):
    """The PCRE package contains Perl Compatible Regular Expression
    libraries. These are useful for implementing regular expression
    pattern matching using the same syntax and semantics as Perl 5."""

    homepage = "http://www.pcre.org"
    url      = "https://ftp.pcre.org/pub/pcre/pcre-8.40.tar.bz2"

    version('8.40', '41a842bf7dcecd6634219336e2167d1d')
    version('8.39', 'e3fca7650a0556a2647821679d81f585')
    version('8.38', '00aabbfe56d5a48b270f999b508c5ad2')

    patch('intel.patch', when='@8.38')

    variant('utf', default=True,
            description='Enable support for UTF-8/16/32, '
            'incompatible with EBCDIC.')
    variant('pcre16', default=True,
            description='Build 16 bit pcre library.')
    variant('pcre32', default=True,
            description='Build 32 bit pcre library.')
    variant('jit', default=True,
            description='Support just-in-time compilation')
    variant('zlib', default=True,
            description='Link pcregrep with libz to handle .gz files')
    variant('bzip2', default=True,
            description='Link pcregrep with libbz2 to handle .bz2 files')
    variant('readline', default=True,
            description='Link pcretest program to readline')

    depends_on('zlib', when='+zlib')
    depends_on('bzip2', when='+bzip2')
    depends_on('readline', when='+readline')

    def configure_args(self):
        args = []
        if '+utf' in self.spec:
            args.append('--enable-utf')
            args.append('--enable-unicode-properties')
        if '+pcre16' in self.spec:
            args.append('--enable-pcre16')
        if '+pcre32' in self.spec:
            args.append('--enable-pcre32')
        if '+jit' in self.spec:
            args.append('--enable-jit')
        if '+zlib' in self.spec:
            args.append('--enable-pcregrep-libz')
        if '+bzip2' in self.spec:
            args.append('--enable-pcregrep-libbz2')
        if '+readline' in self.spec:
            args.append('--enable-pcretest-libreadline')
        return args
