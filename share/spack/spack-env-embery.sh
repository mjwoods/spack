# Startup commands for bash shell started by spack-sh
. ~/.bashrc

# Strip /apps wrappers and other unnecessary items from PATH:
export PATH=/bin:/usr/bin:/usr/sbin:/sbin

# Add spack shell support:
export SPACK_ROOT=/g/ns/rd/rdshare/spack/rhel6
. $SPACK_ROOT/share/spack/setup-env.sh

umask 0002

