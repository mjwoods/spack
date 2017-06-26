#!/bin/bash
# Source this file to setup spack shell environment

# Create environment for spack
export SPACK_FRONT_END=haswell
export SPACK_BACK_END=haswell
export SPACK_ROOT=/g/sc/projects_lustre/pr_nwp/mwoods/spack

# Remove compilers from environment:
module unload PrgEnv-cray PrgEnv-gnu PrgEnv-intel cray gcc intel

# Ensure that modulecmd is in PATH:
export PATH="$SPACK_ROOT/bin:$PATH:/opt/modules/default/bin"

. "$SPACK_ROOT/share/spack/setup-env.sh"

umask 0002
