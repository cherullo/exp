from pathlib import Path

class ReportPath():
    def __init__(self, base, *args):
        self.path = Path(base).joinpath(*args).resolve()

        self.path.mkdir(parents = True, exist_ok=True)

    def get(self, filename:str = None) -> str:

        if (filename == None):
            return str(self.path)

        return str(self.path.joinpath(filename))



