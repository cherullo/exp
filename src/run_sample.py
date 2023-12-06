import sys
import os

if (__name__ == "__main__"):

    # Reduce tensorflow verbosity
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

    # Add /src to PYTHONPATH
    myPath = os.path.dirname(__file__)
    sys.path.append(myPath)

    if "PYTHONPATH" in os.environ:
        os.environ["PYTHONPATH"] += os.pathsep + myPath
    else:
        os.environ["PYTHONPATH"] = myPath

    # Get the path of the file to run and make it absolute
    toRun = sys.argv[1]
    if (os.path.isabs(toRun) == False):
        toRun = os.path.abspath(os.path.join(os.getcwd(), toRun))

    # Change dir to file to run
    toRunPath = os.path.dirname(toRun)
    os.chdir(toRunPath)

    os.system("python " + toRun)


