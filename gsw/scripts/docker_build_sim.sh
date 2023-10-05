#!/bin/bash -i
#
# Convenience script for NOS3 development
# Use with the Dockerfile in the deployment repository
# https://github.com/nasa-itc/deployment
#

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source $SCRIPT_DIR/env.sh

mkdir -p $BASE_DIR/sims/build
$DFLAGS_CPUS -v $BASE_DIR:$BASE_DIR --name "nos_build_sim" -w $BASE_DIR ivvitc/nos3 make -j$NUM_CPUS build-sim