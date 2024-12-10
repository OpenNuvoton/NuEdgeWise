#  Copyright (c) 2021 Arm Limited. All rights reserved.
#  SPDX-License-Identifier: Apache-2.0
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Utility script to generate model c file that can be included in the
project directly. This should be called as part of cmake framework
should the models need to be generated at configuration stage.
"""
import datetime
import os
from argparse import ArgumentParser
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import binascii

parser = ArgumentParser()

parser.add_argument("--tflite_path", help="Model (.tflite) path", required=True)
parser.add_argument("--output_dir", help="Output directory", required=True)
parser.add_argument("--template_dir", type=str, help="Template files directory", required=True)
parser.add_argument('-e', '--expression', action='append', default=[], dest="expr")
parser.add_argument('--header', action='append', default=[], dest="headers")
parser.add_argument('-ns', '--namespaces', action='append', default=[], dest="namespaces")
parser.add_argument("--license_template", type=str, help="Header template file",
                    default="header_template.txt")
args = parser.parse_args()

env = Environment(loader=FileSystemLoader(args.template_dir),
                  trim_blocks=True,
                  lstrip_blocks=True)


def get_tflite_data(tflite_path: str) -> list:
    """
    Reads a binary file and returns a C style array as a
    list of strings.

    Argument:
        tflite_path:    path to the tflite model.

    Returns:
        list of strings
    """
    with open(tflite_path, 'rb') as tflite_model:
        data = tflite_model.read()

    bytes_per_line = 32
    hex_digits_per_line = bytes_per_line * 2
    hexstream = binascii.hexlify(data).decode('utf-8')
    hexstring = '{'

    for i in range(0, len(hexstream), 2):
        if 0 == (i % hex_digits_per_line):
            hexstring += "\n"
        hexstring += '0x' + hexstream[i:i+2] + ", "

    hexstring += '};\n'
    return [hexstring]


def main(args):
    if not os.path.isfile(args.tflite_path):
        raise Exception(f"{args.tflite_path} not found")

    # Cpp filename:
    cpp_filename = Path(os.path.join(args.output_dir, os.path.basename(args.tflite_path) + ".cc")).absolute()
    print(f"++ Converting {os.path.basename(args.tflite_path)} to\
    {os.path.basename(cpp_filename)}")

    os.makedirs(cpp_filename.parent, exist_ok=True)

    header_template = env.get_template(args.license_template)

    hdr = header_template.render(script_name=os.path.basename(__file__),
                                 file_name=os.path.basename(args.tflite_path),
                                 gen_time=datetime.datetime.now(),
                                 year=datetime.datetime.now().year)

    env.get_template('tflite.cc.template').stream(common_template_header=hdr,
                                                  model_data=get_tflite_data(args.tflite_path),
                                                  expressions=args.expr,
                                                  additional_headers=args.headers,
                                                  namespaces=args.namespaces).dump(str(cpp_filename))


if __name__ == '__main__':
    main(args)
