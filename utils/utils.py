import os
from pathlib import Path
import yaml
import re


__location__ = Path(os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))))

loader = yaml.SafeLoader
loader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))

def load_params():
    # fn = __location__.joinpath("../params.yaml")
    fn = __location__.joinpath("../config.yaml")
    with open(fn) as f:
        params = yaml.load(f, Loader=loader)
    return params