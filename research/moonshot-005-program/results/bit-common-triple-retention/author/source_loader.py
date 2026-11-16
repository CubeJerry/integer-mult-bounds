"""Load a pinned repository verifier or price module without mutating it."""
import importlib.util


def load(path, name):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module
