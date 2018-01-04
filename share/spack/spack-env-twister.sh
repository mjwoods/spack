# Startup commands for bash shell started by spack-sh
. ~/.bashrc
module purge

# Make files NOT group-writeable by default:
umask 0022

# Strip /apps wrappers and other unnecessary items from PATH:
export PATH=/bin:/usr/bin:/usr/sbin:/sbin

# System python is too old; use newer version from /apps:
export PATH=/apps/python/2.7.5/bin:$PATH

# Add spack shell support:
export SPACK_ROOT=/rtop/dev/mwoods/spack
. $SPACK_ROOT/share/spack/setup-env.sh

# Use up-to-date curl and openssl with the ca-bundle.crt from RHEL7 (logan),
# to avoid SSL errors from outdated RHEL5 curl:
module load curl-7.54.0-gcc-4.4.7-korhvrj
export CURL_CA_BUNDLE=/rtop/dev/mwoods/spack/opt/linux-rhel5-x86_64/gcc-4.4.7/openssl-1.0.2k-u4wuxmvpr7jupzwbmm4fh4mn4cemj5uj/etc/openssl/certs/ca-bundle.crt

# Use up-to-date tar to allow newer compression formats:
module load tar-1.29-gcc-4.4.7-eovrwho

# Use up-to-date binutils to allow linking of newer packages:
#module load binutils-2.28-gcc-4.4.7-w6wrg2o

