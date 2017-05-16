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
import platform
import os
import sys


class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""
    homepage = 'http://qt.io'
    url      = 'http://download.qt.io/archive/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.gz'
    list_url = 'http://download.qt.io/archive/qt/'
    list_depth = 3

    version('5.7.1',  '031fb3fd0c3cc0f1082644492683f18d')
    version('5.7.0',  '9a46cce61fc64c20c3ac0a0e0fa41b42')
    version('5.5.1',  '59f0216819152b77536cf660b015d784')
    version('5.4.2',  'fa1c4d819b401b267eb246a543a63ea5')
    version('5.4.0',  'e8654e4b37dd98039ba20da7a53877e6')
    version('5.3.2',  'febb001129927a70174467ecb508a682')
    version('5.2.1',  'a78408c887c04c34ce615da690e0b4c8')
    version('4.8.6',  '2edbe4d6c2eff33ef91732602f3518eb')
    version('3.3.8b', '9f05b4125cfe477cc52c9742c3c09009')

    # Add patch for compile issues with qt3 found with use in the
    # OpenSpeedShop project
    variant('krellpatch', default=False,
            description="Build with openspeedshop based patch.")
    variant('mesa',       default=False,
            description="Depend on mesa.")
    variant('gtk',        default=False,
            description="Build with gtkplus.")
    variant('webkit',     default=False,
            description="Build the Webkit extension")
    variant('examples',   default=False,
            description="Build examples.")
    variant('dbus',       default=False,
            description="Build with D-Bus support.")
    variant('phonon',     default=False,
            description="Build with phonon support.")
    variant('x11', default=True if sys.platform != 'darwin' else False,
            description="Build with X11 support.")

    patch('qt3accept.patch', when='@3.3.8b')
    patch('qt3cstddef.patch', when='@3.3.8b')
    patch('qt3krell.patch', when='@3.3.8b+krellpatch')
    patch('qt3xrandr.patch', when='@3.3.8b+x11')

    # https://github.com/xboxdrv/xboxdrv/issues/188
    patch('btn_trigger_happy.patch', when='@5.7.0:')

    patch('qt4-corewlan-new-osx.patch', when='@4')
    patch('qt4-pcre-include-conflict.patch', when='@4')
    patch('qt4-el-capitan.patch', when='@4')

    # Use system openssl for security.
    depends_on("openssl")

    depends_on("glib", when='@4:')
    depends_on("pcre@8.38", when="@5:5.7.9")
    depends_on("pcre@8.40", when="@5.8:")  

    depends_on("gtkplus", when='+gtk')
    depends_on("libxml2")
    depends_on("zlib")
    depends_on("dbus", when='@4:+dbus')
    depends_on("libtiff")
    depends_on("libpng@1.2.57", when='@3')
    depends_on("libpng", when='@4:')
    depends_on("libmng")
    depends_on("jpeg")
    depends_on("icu4c")
    depends_on("harfbuzz", when='@5:')
    depends_on("freetype")

    # QtQml
    depends_on("python", when='@5.7.0:', type='build')

    # OpenGL hardware acceleration
    depends_on("mesa", when='+mesa')
    depends_on("mesa-glu", when='+mesa')
    depends_on("libxmu", when='+mesa')

    # Webkit
    depends_on("flex", when='+webkit', type='build')
    depends_on("bison", when='+webkit', type='build')
    depends_on("gperf", when='+webkit')
    depends_on("fontconfig", when='+webkit')

    # X11 build requirements based on:
    #   http://doc.qt.io/qt-4.8/requirements-x11.html
    #   http://doc.qt.io/qt-5/linux-requirements.html
    # Some of these packages may not be needed in certain qt builds,
    # but installing and building with them should be harmless.
    depends_on("libxrender", when='+x11')
    depends_on("libxrandr", when='+x11')
    depends_on("libxcursor", when='+x11')
    depends_on("libxfixes", when='+x11')
    depends_on("libxinerama", when='+x11')
    depends_on("fontconfig", when='+x11')
    depends_on("libxi", when='+x11')
    depends_on("libxt", when='+x11')
    depends_on("libxext", when='+x11')
    depends_on("libx11", when='+x11')
    depends_on("libsm", when='+x11')
    depends_on("libice", when='+x11')
    depends_on("libxft", when='+x11')
    depends_on("libxv", when='+x11')

    depends_on("libxcb", when='@5:+x11')
    depends_on("xcb-util-image", when='@5:+x11')
    depends_on("xcb-util-keysyms", when='@5:+x11')
    depends_on("xcb-util-renderutil", when='@5:+x11')
    depends_on("xcb-util-wm", when='@5:+x11')

    # qt-5.7 requires a compiler that complies with the c++-11 standard.
    # gcc-4.7 supports some of the standard; later versions are preferred.
    conflicts("%gcc@:4.7", when='@5.7:')

    # Multimedia
    # depends_on("gstreamer", when='+multimedia')
    # depends_on("pulse", when='+multimedia')
    # depends_on("flac", when='+multimedia')
    # depends_on("ogg", when='+multimedia')

    use_xcode = True

    def url_for_version(self, version):
        # URL keeps getting more complicated with every release
        url = self.list_url

        if version >= Version('4.0'):
            url += version.up_to(2) + '/'
        else:
            url += version.up_to(1) + '/'

        if version >= Version('4.8'):
            url += str(version) + '/'

        if version >= Version('5'):
            url += 'single/'

        url += 'qt-'

        if version >= Version('4.6'):
            url += 'everywhere-'
        elif version >= Version('2.1'):
            url += 'x11-'

        if version >= Version('4.0'):
            url += 'opensource-src-'
        elif version >= Version('3'):
            url += 'free-'

        url += str(version) + '.tar.gz'

        return url

    def setup_environment(self, spack_env, run_env):
        run_env.set('QTDIR', self.prefix)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('QTDIR', self.prefix)

    def setup_dependent_package(self, module, dependent_spec):
        module.qmake = Executable(join_path(self.spec.prefix.bin, 'qmake'))

    def patch(self):
        if self.spec.satisfies('@4'):
            # Fix qmake compilers in the default mkspec
            filter_file('^QMAKE_CC .*', 'QMAKE_CC = cc',
                        'mkspecs/common/g++-base.conf')
            filter_file('^QMAKE_CXX .*', 'QMAKE_CXX = c++',
                        'mkspecs/common/g++-base.conf')

            # Necessary to build with GCC 6 and other modern compilers
            # http://stackoverflow.com/questions/10354371/
            filter_file('(^QMAKE_CXXFLAGS .*)', r'\1 -std=gnu++98',
                        'mkspecs/common/gcc-base.conf')

            filter_file('^QMAKE_LFLAGS_NOUNDEF .*', 'QMAKE_LFLAGS_NOUNDEF = ',
                        'mkspecs/common/g++-unix.conf')
        elif self.spec.satisfies('@5:'):
            # Fix qmake compilers in the default mkspec
            filter_file('^QMAKE_COMPILER .*', 'QMAKE_COMPILER = cc',
                        'qtbase/mkspecs/common/g++-base.conf')
            filter_file('^QMAKE_CC .*', 'QMAKE_CC = cc',
                        'qtbase/mkspecs/common/g++-base.conf')
            filter_file('^QMAKE_CXX .*', 'QMAKE_CXX = c++',
                        'qtbase/mkspecs/common/g++-base.conf')

            filter_file('^QMAKE_LFLAGS_NOUNDEF .*', 'QMAKE_LFLAGS_NOUNDEF = ',
                        'qtbase/mkspecs/common/g++-unix.conf')

    @property
    def common_config_args(self):
        config_args = [
            '-prefix', self.prefix,
            '-v',
            '-opensource',
            '-opengl',
            '-release',
            '-shared',
            '-confirm-license',
            '-openssl-linked',
            '-optimized-qmake',
            '-no-openvg',
            '-no-pch',
        ]

        if '@:5.7.0' in self.spec:
            config_args.extend([
                # NIS is deprecated in more recent glibc,
                # but qt-5.7.1 does not recognize this option
                '-no-nis',
            ])

        if '~examples' in self.spec:
            config_args.extend(['-nomake', 'examples'])

        if '@4' in self.spec and '~phonon' in self.spec:
            config_args.append('-no-phonon')

        if '+dbus' in self.spec:
            dbus = self.spec['dbus'].prefix
            config_args.append('-dbus-linked')
            config_args.append('-I%s/dbus-1.0/include' % dbus.lib)
            config_args.append('-I%s/dbus-1.0' % dbus.include)
            config_args.append('-L%s' % dbus.lib)
            config_args.append('-ldbus-1')
        else:
            config_args.append('-no-dbus')

        if '@5:' in self.spec and sys.platform == 'darwin':
            config_args.extend([
                '-no-xinput2',
                '-no-xcb-xlib',
                '-no-pulseaudio',
                '-no-alsa',
            ])

        if '@4' in self.spec and sys.platform == 'darwin':
            config_args.append('-cocoa')

            mac_ver = tuple(platform.mac_ver()[0].split('.')[:2])
            sdkname = 'macosx%s' % '.'.join(mac_ver)
            sdkpath = which('xcrun')('--show-sdk-path',
                                     '--sdk', sdkname,
                                     output=str)
            config_args.extend([
                '-sdk', sdkpath.strip(),
            ])
            use_clang_platform = False
            if self.spec.compiler.name == 'clang' and \
               str(self.spec.compiler.version).endswith('-apple'):
                use_clang_platform = True
            # No one uses gcc-4.2.1 anymore; this is clang.
            if self.spec.compiler.name == 'gcc' and \
               str(self.spec.compiler.version) == '4.2.1':
                use_clang_platform = True
            if use_clang_platform:
                config_args.append('-platform')
                if mac_ver >= (10, 9):
                    config_args.append('unsupported/macx-clang-libc++')
                else:
                    config_args.append('unsupported/macx-clang')

        return config_args

    # Don't disable all the database drivers, but should
    # really get them into spack at some point.

    @when('@3')  # noqa: F811
    def configure(self):
        # A user reported that this was necessary to link Qt3 on ubuntu.
        # However, if LD_LIBRARY_PATH is not set the qt build fails, check
        # and set LD_LIBRARY_PATH if not set, update if it is set.
        if os.environ.get('LD_LIBRARY_PATH'):
            os.environ['LD_LIBRARY_PATH'] += os.pathsep + os.getcwd() + '/lib'
        else:
            os.environ['LD_LIBRARY_PATH'] = os.pathsep + os.getcwd() + '/lib'
        spec = self.spec
        libs = []
        if spec.satisfies('+x11'):
            libs += ['libsm', 'libxext', 'libxinerama', 'libxcursor',
                     'libxrandr', 'randrproto', 'libxrender',
                     'libx11', 'libxft', 'freetype', 'fontconfig']
        if spec.satisfies('+mesa'):
             libs += ['mesa', 'mesa-glu', 'libxmu']
        args = map(lambda lib: "-I%s" % spec[lib].prefix.include, libs) \
               + map(lambda lib: "-L%s" % spec[lib].prefix.lib, libs)
        configure('-prefix', self.prefix,
                  '-v',
                  '-thread',
                  '-shared',
                  '-release',
                  '-fast',
                  *args)

    @when('@4')  # noqa: F811
    def configure(self):
        configure('-fast',
                  '-{0}gtkstyle'.format('' if '+gtk' in self.spec else 'no-'),
                  '-{0}webkit'.format('' if '+webkit' in self.spec else 'no-'),
                  '-arch', str(self.spec.architecture.target),
                  *self.common_config_args)

    @when('@5.0:5.6')  # noqa: F811
    def configure(self):
        webkit_args = [] if '+webkit' in self.spec else ['-skip', 'qtwebkit']
        gcc_args =  ['-no-c++11'] if '%gcc@:4.7' in self.spec else []
        configure('-no-eglfs',
                  '-no-directfb',
                  '-{0}gtkstyle'.format('' if '+gtk' in self.spec else 'no-'),
                  *(gcc_args + webkit_args + self.common_config_args))

    @when('@5.7:')  # noqa: F811
    def configure(self):
        config_args = self.common_config_args

        if '~webkit' in self.spec:
            config_args.extend([
                '-skip', 'webengine',
            ])

        configure('-no-eglfs',
                  '-no-directfb',
                  '-{0}gtk'.format('' if '+gtk' in self.spec else 'no-'),
                  *config_args)

    def install(self, spec, prefix):
        self.configure()
        make()
        make("install")
