#!/usr/bin/env bash
cd "$(dirname "$0")"
set -x
set -u

LLVM_VERSION="$1"
LLVM_URL=https://releases.llvm.org/$LLVM_VERSION/llvm-$LLVM_VERSION.src.tar.xz
CLANG_URL=https://releases.llvm.org/$LLVM_VERSION/cfe-$LLVM_VERSION.src.tar.xz

CMAKE_SERIES=3.4
CMAKE_VERSION=${CMAKE_SERIES}.3

ARCHES=( x86_64 i686 arm64 armv7 armv6 )

# setup llvm/clang source
rm -rf llvm-$LLVM_VERSION.src
wget $LLVM_URL
wget $CLANG_URL
unxz *.tar.xz
tar xvf llvm*.tar
tar xvf cfe*.tar
mv cfe-$LLVM_VERSION.src llvm-$LLVM_VERSION.src/tools/clang
rm *.tar

for ARCH in "${ARCHES[@]}"
do
    DOCKER_IMAGE=linux-$ARCH
    if [ $ARCH = x86_64 ]; then
        DOCKER_IMAGE=manylinux-x64
    elif [ $ARCH = i686 ]; then
        DOCKER_IMAGE=manylinux-x86
    fi

    docker run -v$PWD:/build \
               -w/build \
               --user $UID:$UID \
               --rm -t dockcross/$DOCKER_IMAGE \
               ./llvm-build.sh $LLVM_VERSION $ARCH

    cd install_$ARCH
    zip -r llvm-$LLVM_VERSION-Linux-$ARCH.zip llvm-$LLVM_VERSION-Linux-$ARCH
done
