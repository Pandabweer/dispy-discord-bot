import yaml
import os

from dotenv import load_dotenv

load_dotenv()


def _env_var_constructor(loader, node):
    default = None

    # Check if the node is a plain string value
    if node.id == 'scalar':
        value = loader.construct_scalar(node)
        key = str(value)
    else:
        # The node value is a list
        value = loader.construct_sequence(node)

        if len(value) >= 2:
            # If we have at least two values, then we have both a key and a default value
            default = value[1]
            key = value[0]
        else:
            # Otherwise, we just have a key
            key = value[0]

    return os.getenv(key, default)


yaml.SafeLoader.add_constructor("!ENV", _env_var_constructor)

with open("config.yml", encoding="UTF-8") as f:
    _CONFIG_YAML = yaml.safe_load(f)


def _obj_dic(d: dict):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, _obj_dic(j))
        elif isinstance(j, seqs):
            setattr(top, i,
                    type(j)(_obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top


config = _obj_dic(_CONFIG_YAML)
