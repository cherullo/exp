import sys
import os

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

    # Reduce tensorflow verbosity
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

    # Add /src to PYTHON_PATH
    myPath = os.path.dirname(__file__)
    sys.path.append(myPath)

    # Get the path of the file to run and make it absolute
    toRun = sys.argv[1]
    if (os.path.isabs(toRun) == False):
        toRun = os.path.abspath(os.path.join(os.getcwd(), toRun))

    # Change dir to file to run
    toRunPath = os.path.dirname(toRun)
    os.chdir(toRunPath)
    sys.path.append(toRunPath)

    execfile(toRun)


