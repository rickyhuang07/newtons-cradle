import importlib.metadata

class DistributionNotFound(Exception):
    pass


class V:
    pass

def get_distribution(x):
    o = V()
    o.version = importlib.metadata.version(x)
    return o
