import sys
from os import path, chdir, getcwd

def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

if (__name__ == "__main__"):

    # Add /src to PYTHON_PATH
    myPath = path.dirname(__file__)
    sys.path.append(myPath)

    # Get the path of the file to run and make it absolute
    toRun = sys.argv[1]
    if (path.isabs(toRun) == False):
        toRun = path.abspath(path.join(getcwd(), toRun))

    # Change dir to file to run
    toRunPath = path.dirname(toRun)
    chdir(toRunPath)
    sys.path.append(toRunPath)

    execfile(toRun)


