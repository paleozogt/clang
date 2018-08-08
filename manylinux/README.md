Sadly there's no official `manylinux1` builds of LLVM or Clang.

These scripts build LLVM and Clang using the [manylinux1](https://github.com/pypa/manylinux) (aka Centos 5) images and produce zip files of the installation.

The build script takes the LLVM version to build.

To build make sure you have Docker installed, then

```
> ./build.sh 6.0.1
```

and wait a while.  By the end you'll have two zip files:

```
> ls *.zip
llvm-6.0.1-Linux-x86_64.zip llvm-6.0.1-Linux-i686.zip
```
