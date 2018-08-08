#!/usr/bin/env bash
cd "$(dirname "$0")"
set -x
set -u

LLVM_VERSION="$1"
LLVM_URL=https://releases.llvm.org/$LLVM_VERSION/llvm-$LLVM_VERSION.src.tar.xz
CLANG_URL=https://releases.llvm.org/$LLVM_VERSION/cfe-$LLVM_VERSION.src.tar.xz

CMAKE_SERIES=3.4
CMAKE_VERSION=${CMAKE_SERIES}.3

ARCHES=( x86_64 i686 )

# setup llvm/clang source
rm -rf llvm-$LLVM_VERSION.src
wget $LLVM_URL
wget $CLANG_URL
unxz *.tar.xz
tar xvf llvm*.tar
tar xvf cfe*.tar
mv cfe-$LLVM_VERSION.src llvm-$LLVM_VERSION.src/tools/clang
rm *.tar

# setup cmake
for ARCH in "${ARCHES[@]}"
do
    CMAKE_ARCH=$ARCH
    if [ $ARCH = i686 ]; then
        CMAKE_ARCH=i386
    fi    
    CMAKE_URL=https://cmake.org/files/v$CMAKE_SERIES/cmake-$CMAKE_VERSION-Linux-$CMAKE_ARCH.tar.gz

    # setup cmake
    rm -rf cmake_$ARCH
    wget $CMAKE_URL
    tar xvf cmake-*.tar.gz
    mv cmake-$CMAKE_VERSION-Linux-$CMAKE_ARCH cmake_$ARCH
    rm *.tar.gz
done

for ARCH in "${ARCHES[@]}"
do
    docker run -v$PWD:/build \
               -w/build \
               --user $UID:$UID \
               --rm -t quay.io/pypa/manylinux1_$ARCH \
               ./llvm-build.sh $LLVM_VERSION

    cd install_$ARCH
    zip -r llvm-$LLVM_VERSION-Linux-$ARCH.zip llvm-$LLVM_VERSION-Linux-$ARCH
done
