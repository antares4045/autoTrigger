from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import os

files_in_project = []

for basefolder in os.listdir('./'):
    if(os.path.isdir(basefolder)):
        for folder, subfolders, files in os.walk(basefolder):
            for file in files:
                if file[-3:] == '.py' and file != '__init__.py':
                    path_to_file = os.path.join(folder, file)
                    packname = '.'.join(folder.split(
                        os.path.sep) + [file[:-3]])
                    files_in_project.append([packname, path_to_file])

ext_modules = [
    Extension(packname, [path_to_file])
    for packname, path_to_file in files_in_project
]

setup(
    name='Test App',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
# C:/Anaconda3/python.exe d:/prog/py/grabscrren/compile.py build_ext --inplace
