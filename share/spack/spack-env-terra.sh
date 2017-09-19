#!/bin/bash
# Source this file to setup spack shell environment

# Create environment for spack
export SPACK_FRONT_END=haswell
export SPACK_BACK_END=haswell
export SPACK_ROOT=/g/sc/projects_lustre/pr_rdshare/spack

# Remove compilers from environment:
module unload PrgEnv-cray PrgEnv-gnu PrgEnv-intel cray gcc intel

# Ensure that modulecmd is in PATH:
export PATH="$SPACK_ROOT/bin:$PATH:/opt/modules/default/bin"

. "$SPACK_ROOT/share/spack/setup-env.sh"

# We seem to have a bug in setup-env.sh with our version of bash,
# because MODULEPATH is not set correctly unless we do it here:
module use "$SPACK_ROOT/share/spack/modules/cray-CNL-haswell"

umask 0002
