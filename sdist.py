import sys
import os
import shutil
import zipfile
from download_deps import download_deps

llvm_version='.'.join(open('version.txt').read().split('.')[:3])

setup_py='''
from setuptools import setup
setup(
    name="clang",
    version="%s",
    package_data={ 'clang' : ['*'] },
    packages=["clang"],
)
''' % (llvm_version)

def zipdir(path, inzippath, outfile):
    zip = zipfile.ZipFile(outfile, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            file = os.path.join(root, file)
            zip.write(file, file.replace(path, inzippath))

def main():
    plat_name = None
    if len(sys.argv) > 1:
        plat_name = sys.argv[1]

    build_dir = "build"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.mkdir(build_dir)

    open(os.path.join(build_dir, "setup.py"), "w").write(setup_py)
    download_deps(plat_name)
    shutil.copytree("clang", os.path.join(build_dir, "clang"))

    dist_dir = "dist"    
    if not os.path.exists(dist_dir):
        os.mkdir(dist_dir)
    zipdir(build_dir, "clang", os.path.join(dist_dir, "%s_%s.zip" % ("clang", plat_name)))

if __name__ == "__main__":
    main()
