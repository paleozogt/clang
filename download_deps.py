import sys
import errno
import os
from os import path
from shutil import copy
from distutils.dir_util import copy_tree
from glob import glob
from subprocess import call
import libarchive.public
from inspect import cleandoc

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


llvm_version='.'.join(open('version.txt').read().split('.')[:3])

clang_binary_urls = {
    "mac" : {
        "64" : "https://homebrew.bintray.com/bottles/llvm-%s.el_capitan.bottle.tar.gz" % llvm_version
    },
    "linux" : {
        "32" : "https://ethanhs.me/static/llvm-%s-Linux-i686.zip" % llvm_version,
        "64" : "https://ethanhs.me/static/llvm-%s-Linux-x86_64.zip" % llvm_version
    },
    "win" : {
        "32" : "http://releases.llvm.org/%s/LLVM-%s-win32.exe" % (llvm_version, llvm_version),
        "64" : "http://releases.llvm.org/%s/LLVM-%s-win64.exe" % (llvm_version, llvm_version)
    }
}

def get_clang_binary_url(plat_name):
    if "mac" in plat_name:
        return clang_binary_urls["mac"]["64"]
    elif "linux" in plat_name and "i686" in plat_name:
        return clang_binary_urls["linux"]["32"]
    elif "linux" in plat_name and "x86_64" in plat_name:
        return clang_binary_urls["linux"]["64"]
    elif "win" in plat_name and "win32" in plat_name:
        return clang_binary_urls["win"]["32"]
    elif "win" in plat_name and "amd64" in plat_name:
        return clang_binary_urls["win"]["64"]

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def get_archive_extract_dir(archive_path):
    path_set= set()

    with libarchive.public.file_reader(archive_path) as a:
        for entry in a:
            path_set.add(path.join(entry.pathname.split('/')[0], ''))

    if len(path_set) is 1:
        return next(iter(path_set))
    else:
        return ""

def extract_archive(archive_path):
    print("extracting %s" % archive_path)
    archive_ext = path.splitext(archive_path)[1]

    if archive_ext == '.exe':
        extract_path= path.join(path.splitext(archive_path)[0], '')
    
        # sadly there's no support for NSIS installer extraction in python,
        # so we have to lean on the 7z tool
        cmd = ["7z", "x", archive_path, "-o"+extract_path]
        print(' '.join(cmd))
        call(cmd)
    else:
        extract_path = get_archive_extract_dir(archive_path)
        with libarchive.public.file_reader(archive_path) as a:
            for entry in a:
                print("\t %s" % (entry.pathname))
                if entry.filetype.IFDIR:
                    mkdir_p(entry.pathname)
                else:
                    with open(entry.pathname, 'wb') as f:
                        for block in entry.get_blocks():
                            f.write(block)

    return extract_path

def download_clang_src():
    clang_src="cfe-%s.src" % llvm_version
    clang_src_archive="%s.tar.xz" % clang_src
    clang_src_url= "https://releases.llvm.org/%s/%s" % (llvm_version, clang_src_archive)
    print("downloading %s" % clang_src_url)
    urlretrieve(clang_src_url, clang_src_archive)
    extract_archive(clang_src_archive)

    # deploy clang bindings
    clang_bindings_root=clang_src + "/bindings/python"
    clang_bindings = glob(clang_bindings_root + "/clang/*")
    clang_examples = clang_bindings_root + "/examples"
    clang_tests = clang_bindings_root + "/tests"
    for file in clang_bindings:
        copy(file, 'clang')
    copy_tree(clang_examples, 'examples')
    copy_tree(clang_tests, 'tests')

def hack_clang_libpath(pyfile):
    # default for set_library_path
    with open(pyfile, "a") as f:
        f.write(cleandoc(u'''
        # default library path
        import os
        Config.set_library_path(os.path.dirname(os.path.abspath(__file__)))
        '''))

def download_clang_binary(plat_name):
    clang_binary_url = get_clang_binary_url(plat_name)
    clang_binary_file = path.basename(clang_binary_url)
    print("downloading %s" % clang_binary_url)

    # temp workaround until linux artifacts server can support python downloads
    if "linux" in plat_name:
        cmd= [ "wget", clang_binary_url ]
        print(' '.join(cmd))
        call(cmd)
    else:
        urlretrieve(clang_binary_url, clang_binary_file)

    clang_binary_dir = extract_archive(clang_binary_file)

    if "mac" in plat_name:
        clang_files= glob(clang_binary_dir + "%s/lib/libclang*.dylib" % llvm_version)
    elif "linux" in plat_name:
        clang_files= glob(clang_binary_dir + "lib/libclang*.so*")
    elif "win" in plat_name:
        clang_files=  glob(clang_binary_dir + "bin/libclang*.dll")
        clang_files+= glob(clang_binary_dir + "bin/msvc*.dll")
        clang_files+= glob(clang_binary_dir + "bin/vcruntime*.dll")

    for file in clang_files:
        print("deploying %s" % file)
        copy(file, 'clang')

def download_deps(plat_name):
    print("download_deps " + str(plat_name))
    download_clang_src()
    if plat_name and not plat_name == "any":
        hack_clang_libpath("clang/cindex.py")
        download_clang_binary(plat_name)

def main():
    plat_name = None
    if len(sys.argv) > 1:
        plat_name = sys.argv[1]

    download_deps(plat_name)

if __name__ == "__main__":
    main()
