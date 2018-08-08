#!/usr/bin/env bash
cd "$(dirname "$0")"
set -x
set -u

ARCH=`uname -p`
LLVM_VERSION="$1"

export PATH="/opt/python/cp27-cp27mu/bin:$PWD/cmake_$ARCH/bin:$PATH"

rm -rf build_$ARCH
mkdir -p build_$ARCH
pushd build_$ARCH
cmake $PWD/../llvm-*.src -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$PWD/../llvm-$LLVM_VERSION-Linux-$ARCH

make -j 8
make -j 8 install

popd
