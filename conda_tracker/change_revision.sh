#!/bin/sh
submodule=$1
revision=$2
cd $submodule
git checkout $revision
cd ..