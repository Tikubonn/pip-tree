
import os
import re
import sys 
import json
import argparse
import importlib.metadata
import opensafer
import subprocess

class _PIPTree:

  _REGEXP_PACKAGE_EXPRESSIONS:"typing.ClassVar[re.Pattern]" = [
    re.compile(r"^(\S+)==\S+$"),
    re.compile(r"^(\S+) @ \S+$"),
    re.compile(r"^# Editable install with no version control \((\S+)==\S+\)$"),
    re.compile(r"^(\S+)$"),
  ]
  
  _REGEXP_PIP_SHOW_NAME:"typing.ClassVar[re.Pattern]" = re.compile(r"^Name: (\S+)$")
  _REGEXP_PIP_SHOW_REQUIRES:"typing.ClassVar[re.Pattern]" = re.compile(r"^Requires: (.*)$")

  def __init__ (self):
    self.package_dependency_table = {}
    self.package_table = {}

  def list_installed_package () -> list[str]:
    process = subprocess.run(
      ["pip", "freeze"],
      stdin=subprocess.DEVNULL,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
      check=True
    )
    installed_packages = []
    for line in process.stdout.split("\n"):
      for regexp in self._REGEXP_PACKAGE_EXPRESSIONS:
        match = regexp.match(line)
        if match:
          installed_packages.append(match.group(1))
          break
    return installed_packages

  def get_package_dependencies (self, package:str) -> list[str]:
    if package not in self.package_dependency_table:
      process = subprocess.run(
        ["pip", "show", package],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True
      )
      name = ""
      requires = []
      for line in process.stdout.split("\n"):
        match = self._REGEXP_PIP_SHOW_NAME.match(line)
        if match:
          name, = match.groups()
          continue
        match = self._REGEXP_PIP_SHOW_REQUIRES.match(line)
        if match:
          requires_src, = match.groups()
          if requires_src:
            requires = requires_src.split(", ")
          continue
      self.package_dependency_table[package] = requires
    return self.package_dependency_table[package]

  def get_package (self, package:str) -> "dict[str, typing.Any]":
    if package not in self.package_table:
      metadata = importlib.metadata.metadata(package)
      metadata_dict = metadata.json
      metadata_dict["_dependencies"] = []
      for dependency in self.get_package_dependencies(package):
        pkg = self.get_package(dependency)
        metadata_dict["_dependencies"].append(pkg)
      self.package_table[package] = metadata_dict
    return self.package_table[package]

def dump_package_tree (
  packages:"list[dict[str, typing.Any]]", 
  *, 
  file:"io.TextIOBase", 
  indent:int, 
  _total_indent:int=0):
  for package in packages:
    if 0 < _total_indent:
      indentation = " " * _total_indent + "- "
    else:
      indentation = ""
    print("{:s}{:s}=={:s}".format(
      indentation, 
      package["name"], 
      package["version"]
    ), file=file)
    dump_package_tree(
      package.get("_dependencies", []), 
      file=file, 
      indent=indent, 
      _total_indent=_total_indent + indent
    )

def main ():
  parser = argparse.ArgumentParser(description="Dump installed package info by pip.")
  parser.add_argument("packages", nargs="*", help="Package names for dump.")
  parser.add_argument("--json", action="store_true", help="Dump information as JSON format.")
  parser.add_argument("--indent", nargs="?", default=2, help="Amount of indentation depth.")
  parser.add_argument("-o", "--output-file", type=str, default="", help="Path of output file. (default is stdout).")
  args = parser.parse_args()
  pip_tree = _PIPTree()
  if args.packages:
    packages = args.packages
  else:
    packages = pip_tree.list_installed_package()
  if args.output_file:
    stream = opensafer.open_safer(args.output_file, "w", encoding="utf-8")
  else:
    stream = os.fdopen(os.dup(sys.stdout.fileno()), "w", encoding="utf-8")
  with stream:
    package_tree = [pip_tree.get_package(p) for p in packages]
    if args.json:
      json.dump(package_tree, stream, indent=args.indent)
    else:
      dump_package_tree(package_tree, file=stream, indent=args.indent)

if __name__ == "__main__":
  main()
