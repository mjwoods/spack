#!/bin/bash
# Source this file to setup spack shell environment

# Create environment for spack
export SPACK_FRONT_END=haswell
export SPACK_BACK_END=haswell
export SPACK_ROOT="${SPACK_ROOT-/g/sc/projects_lustre/pr_rdshare/spack}"

# Remove compilers from environment:
module unload PrgEnv-cray PrgEnv-gnu PrgEnv-intel cray gcc intel

# Use a newer python:
export PATH=/g/sc/apps_dev/A1.2.0/python/2.7.5/bin:$PATH

. "$SPACK_ROOT/share/spack/setup-env.sh"

umask 0002
