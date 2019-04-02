# Startup commands for bash shell started by spack-sh
. ~/.bashrc

# Strip /apps wrappers and other unnecessary items from PATH:
export PATH=/bin:/usr/bin:/usr/sbin:/sbin:/home/mwoods/bin

# Setup spack shell support:
export SPACK_ROOT=/g/ns/rd/rdshare/spack/rhel7
. $SPACK_ROOT/share/spack/setup-env.sh

# Provide bzip2 (until provided by OS image):
module load bzip2-1.0.6-gcc-4.8.5-qrd3gzl

umask 0002

