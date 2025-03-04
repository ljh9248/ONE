#!/usr/bin/env python

# Copyright (c) 2020 Samsung Electronics Co., Ltd. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import configparser
import glob
import importlib
import ntpath
import os
import subprocess
import sys

import onelib.constant as _constant


def _add_default_arg(parser):
    # version
    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='show program\'s version number and exit')

    # verbose
    parser.add_argument(
        '-V',
        '--verbose',
        action='store_true',
        help='output additional information to stdout or stderr')

    # configuration file
    parser.add_argument('-C', '--config', type=str, help='run with configuation file')
    # section name that you want to run in configuration file
    parser.add_argument('-S', '--section', type=str, help=argparse.SUPPRESS)


def is_accumulated_arg(arg, driver):
    if driver == "one-quantize":
        accumulables = [
            "tensor_name", "scale", "zero_point", "src_tensor_name", "dst_tensor_name"
        ]
        if arg in accumulables:
            return True

    return False


def _is_valid_attr(args, attr):
    return hasattr(args, attr) and getattr(args, attr)

class Command:
  def __init__(self, driver, args, log_file):
    self.cmd = [driver]
    self.driver = driver
    self.args = args
    self.log_file = log_file

  # Add option if attrs are valid
  # Option values are collected from self.args
  def add_option_with_valid_args(self, option, attrs):
    for attr in attrs:
      if not _is_valid_attr(self.args, attr):
        return self
    self.cmd.append(option)
    for attr in attrs:
      self.cmd.append(getattr(self.args, attr))
    return self

  # Add option and values without any condition
  def add_option_with_values(self, option, values):
    self.cmd.append(option)
    for value in values:
      self.cmd.append(value)
    return self

  # Add option with no argument (ex: --verbose) if attr is valid
  def add_noarg_option_if_valid_arg(self, option, attr):
    if _is_valid_attr(self.args, attr):
      self.cmd.append(option)
    return self

  # Run cmd and save logs
  def run(self):
    self.log_file.write((' '.join(self.cmd) + '\n').encode())
    _run(self.cmd, err_prefix=self.driver, logfile=self.log_file)


def _parse_cfg_and_overwrite(config_path, section, args):
    """
    parse given section of configuration file and set the values of args.
    Even if the values parsed from the configuration file already exist in args,
    the values are overwritten.
    """
    if config_path == None:
        # DO NOTHING
        return
    config = configparser.ConfigParser()
    # make option names case sensitive
    config.optionxform = str
    parsed = config.read(config_path)
    if not parsed:
        raise FileNotFoundError('Not found given configuration file')
    if not config.has_section(section):
        raise AssertionError('configuration file doesn\'t have \'' + section +
                             '\' section')
    for key in config[section]:
        setattr(args, key, config[section][key])
    # TODO support accumulated arguments


def _parse_cfg(args, driver_name):
    """parse configuration file. If the option is directly given to the command line,
       the option is processed prior to the configuration file.
       That is, if the values parsed from the configuration file already exist in args,
       the values are ignored."""
    if _is_valid_attr(args, 'config'):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(args.config)
        # if section is given, verify given section
        if _is_valid_attr(args, 'section'):
            if not config.has_section(args.section):
                raise AssertionError('configuration file must have \'' + driver_name +
                                     '\' section')
            for key in config[args.section]:
                if is_accumulated_arg(key, driver_name):
                    if not _is_valid_attr(args, key):
                        setattr(args, key, [config[args.section][key]])
                    else:
                        getattr(args, key).append(config[args.section][key])
                    continue
                if not _is_valid_attr(args, key):
                    setattr(args, key, config[args.section][key])
        # if section is not given, section name is same with its driver name
        else:
            if not config.has_section(driver_name):
                raise AssertionError('configuration file must have \'' + driver_name +
                                     '\' section')
            secton_to_run = driver_name
            for key in config[secton_to_run]:
                if is_accumulated_arg(key, driver_name):
                    if not _is_valid_attr(args, key):
                        setattr(args, key, [config[secton_to_run][key]])
                    else:
                        getattr(args, key).append(config[secton_to_run][key])
                    continue
                if not _is_valid_attr(args, key):
                    setattr(args, key, config[secton_to_run][key])


def _print_version_and_exit(file_path):
    """print version of the file located in the file_path"""
    script_path = os.path.realpath(file_path)
    dir_path = os.path.dirname(script_path)
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    # run one-version
    subprocess.call([os.path.join(dir_path, 'one-version'), script_name])
    sys.exit()


def _safemain(main, mainpath):
    """execute given method and print with program name for all uncaught exceptions"""
    try:
        main()
    except Exception as e:
        prog_name = os.path.basename(mainpath)
        print(f"{prog_name}: {type(e).__name__}: " + str(e), file=sys.stderr)
        sys.exit(255)


def _run(cmd, err_prefix=None, logfile=None):
    """Execute command in subprocess

    Args:
        cmd: command to be executed in subprocess
        err_prefix: prefix to be put before every stderr lines
        logfile: file stream to which both of stdout and stderr lines will be written
    """
    with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        import select
        inputs = set([p.stdout, p.stderr])
        while inputs:
            readable, _, _ = select.select(inputs, [], [])
            for x in readable:
                line = x.readline()
                if len(line) == 0:
                    inputs.discard(x)
                    continue
                if x == p.stdout:
                    out = sys.stdout
                if x == p.stderr:
                    out = sys.stderr
                    if err_prefix:
                        line = f"{err_prefix}: ".encode() + line
                out.buffer.write(line)
                out.buffer.flush()
                if logfile != None:
                    logfile.write(line)
    if p.returncode != 0:
        sys.exit(p.returncode)


def _remove_prefix(str, prefix):
    if str.startswith(prefix):
        return str[len(prefix):]
    return str


def _remove_suffix(str, suffix):
    if str.endswith(suffix):
        return str[:-len(suffix)]
    return str


def _get_optimization_list(get_name=False):
    """
    returns a list of optimization. If `get_name` is True,
    only basename without extension is returned rather than full file path.

    [one hierarchy]
    one
    ├── backends
    ├── bin
    ├── doc
    ├── include
    ├── lib
    ├── optimization
    └── test

    Optimization options must be placed in `optimization` folder
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # optimization folder
    files = [f for f in glob.glob(dir_path + '/../optimization/O*.cfg', recursive=True)]
    # exclude if the name has space
    files = [s for s in files if not ' ' in s]

    opt_list = []
    for cand in files:
        base = ntpath.basename(cand)
        if os.path.isfile(cand) and os.access(cand, os.R_OK):
            opt_list.append(cand)

    if get_name == True:
        # NOTE the name includes prefix 'O'
        # e.g. O1, O2, ONCHW not just 1, 2, NCHW
        opt_list = [ntpath.basename(f) for f in opt_list]
        opt_list = [_remove_suffix(s, '.cfg') for s in opt_list]

    return opt_list


def _detect_one_import_drivers(search_path):
    """Looks for import drivers in given directory

    Args:
        search_path: path to the directory where to search import drivers

    Returns:
    dict: each entry is related to single detected driver,
          key is a config section name, value is a driver name

    """
    import_drivers_dict = {}
    for module_name in os.listdir(search_path):
        full_path = os.path.join(search_path, module_name)
        if not os.path.isfile(full_path):
            continue
        if module_name.find("one-import-") != 0:
            continue
        module_loader = importlib.machinery.SourceFileLoader(module_name, full_path)
        module_spec = importlib.util.spec_from_loader(module_name, module_loader)
        module = importlib.util.module_from_spec(module_spec)
        try:
            module_loader.exec_module(module)
            if hasattr(module, "get_driver_cfg_section"):
                section = module.get_driver_cfg_section()
                import_drivers_dict[section] = module_name
        except:
            pass
    return import_drivers_dict
