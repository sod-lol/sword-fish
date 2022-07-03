#!/usr/bin/python3

import os
import argparse
import json
from pathlib import Path
import errno

parser = argparse.ArgumentParser(description='Replace all variables inside json with with env variable')

parser.add_argument('--json-config', action='store', type=str, required=True)
parser.add_argument('--output-dir', action='store', type=str, required = True)

args = parser.parse_args()

config_path = Path(args.json-config)

if not config_path.exists():
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.json-config)

if not config_path.isfile():
    raise Exception("Specified json config is not a file")

config_filename = config_path.name
output_file = args.output-dir + "/" + config_filename

def _cast_to_type(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

def substitude_env_vars(d):
    for key in d.keys():
        v = d.get(key)
        if isinstance(v, str):
            m = re.match('\${(\w+)\:-(\w+)}', v)
            if m:
                env_name = m.group(1)
                def_val = m.group(2)
                env_val = os.environ.get(env_name)
                if env_val is None:
                    env_val = _cast_to_type(def_val)
                d[key] = env_val
        elif isinstance(v, dict):
            substitude_env_vars(v)

with open(config_path, 'r+') as config_f:
    json_config = json.load(config_f)
    substitude_env_vars(json_config)
    with open(output_file, 'w+') as output_f:
        output_f.write(json_config)

