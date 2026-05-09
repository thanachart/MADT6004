"""Build .ipynb files from cell lists. ipynb spec: source lines need trailing \n
on all but the last."""
import json
from pathlib import Path

def _to_lines(source):
    if isinstance(source, list):
        source = "\n".join(source)
    lines = source.split("\n")
    out = []
    for i, ln in enumerate(lines):
        out.append(ln + "\n" if i < len(lines) - 1 else ln)
    return out

def cell(kind, source):
    if kind == "md":
        return {"cell_type": "markdown", "metadata": {}, "source": _to_lines(source)}
    return {"cell_type": "code", "metadata": {}, "outputs": [],
            "execution_count": None, "source": _to_lines(source)}

def write_notebook(path, cells):
    nb = {"cells": cells,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python", "version": "3.10"}},
          "nbformat": 4, "nbformat_minor": 5}
    Path(path).write_text(json.dumps(nb, indent=1, ensure_ascii=False))
