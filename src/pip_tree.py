
import re 
import sys 
import json 
import opensafer
import subprocess 
from argparse import ArgumentParser

_REGEXP_PIP_FREEZE_EQUAL:re.Pattern = re.compile(r"^(\S+?)==\S+$")
_REGEXP_PIP_FREEZE_AT:re.Pattern = re.compile(r"^(\S+?) @ .*$")
_REGEXP_PIP_FREEZE_EDITABLE:re.Pattern = re.compile(r"^# Editable install with no version control \((\S+?)==.*$")
_REGEXP_PIP_SHOW_ENTRY:re.Pattern = re.compile(r"(.*?):(.*)")

def _list_installed_package () -> list[str]:
  result = []
  process = subprocess.run(
    ["pip", "freeze"], 
    shell=True, 
    text=True, 
    stdin=subprocess.DEVNULL, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    check=True
  )
  for line in process.stdout.strip().split("\n"):
    match_result = _REGEXP_PIP_FREEZE_EQUAL.match(line)
    if match_result:
      name, = match_result.groups()
      result.append(name)
      continue
    match_result = _REGEXP_PIP_FREEZE_AT.match(line)
    if match_result:
      name, = match_result.groups()
      result.append(name)
      continue
    match_result = _REGEXP_PIP_FREEZE_EDITABLE.match(line)
    if match_result:
      name, = match_result.groups()
      result.append(name)
      continue
  return result

def _get_package_info (package_name:str) -> "dict[str, typing.Any]":
  result = {}
  process = subprocess.run(
    ["pip", "show", package_name], 
    shell=True, 
    text=True, 
    stdin=subprocess.DEVNULL, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    check=True
  )
  for line in process.stdout.strip().split("\n"):
    match_result = _REGEXP_PIP_SHOW_ENTRY.match(line)
    if match_result:
      key, value = map(str.strip, match_result.groups())
      if value:
        if key == "Requires":
          result[key] = [p.strip() for p in value.split(",")]
        elif key == "Required-by":
          result[key] = [p.strip() for p in value.split(",")]
        else:
          result[key] = value
  return result

def _get_package_info_tree (package_names:list[str]) -> "list[dict[str, typing.Any]]":
  package_infos = list()
  package_info_table = dict()
  for package_name in package_names:
    if package_name not in package_info_table:
      package_info_table[package_name] = _get_package_info(package_name)
    package_infos.append(package_info_table[package_name])
  tmp = package_infos[:]
  while tmp:
    package_info = tmp.pop()
    if "_Dependencies" not in package_info:
      for pkg in package_info.get("Requires", []):
        if pkg not in package_info_table:
          package_info_table[pkg] = _get_package_info(pkg)
        pkg_info = package_info_table[pkg]
        package_info.setdefault("_Dependencies", [])
        package_info["_Dependencies"].append(pkg_info)
        tmp.append(pkg_info)
  return package_infos

def _dump_package_info_tree (
  package_infos:"list[dict[str, typing.Any]]", 
  *, 
  file:"io.TextIOBase", 
  indent:int, 
  _total_indent:int=0):
  for packageinfo in package_infos:
    if 0 < _total_indent:
      indentation = "{:s}- ".format(" " * _total_indent)
    else:
      indentation = ""
    print("{:s}{:s}=={:s}".format(
      indentation, 
      packageinfo["Name"],
      packageinfo["Version"]
    ), file=file)
    _dump_package_info_tree(
      packageinfo.get("_Dependencies", []), 
      indent=indent, 
      file=file,
      _total_indent=_total_indent + indent
    )

def main ():
  parser = ArgumentParser(description="Dump installed package info by pip.")
  parser.add_argument("packages", nargs="*", help="Package names for dump.")
  parser.add_argument("--json", action="store_true", help="Dump information as JSON format.")
  parser.add_argument("--indent", nargs="?", default=2, help="Amount of indentation depth.")
  parser.add_argument("--dump-root-only", action="store_true", help="If enabled, show root packages only.")
  parser.add_argument("-o", "--output-file", type=str, default="", help="Path of output file. (default is stdout).")
  args = parser.parse_args()
  if args.packages:
    packages = args.packages
  else:
    packages = _list_installed_package()
  package_infos = _get_package_info_tree(packages)
  if args.dump_root_only: #--dump-root-onlyが真ならば親をもたないパッケージのみ抽出する。
    package_infos = [package_info for package_info in package_infos if not package_info.get("Required-by", [])]
  if args.output_file:
    stream = opensafer.open_safer(args.output_file, "w", encoding="utf-8")
  else:
    stream = sys.stdout
  with stream:
    if args.json:
      json.dump(package_infos, stream, indent=args.indent)
    else:
      _dump_package_info_tree(package_infos, file=stream, indent=args.indent)

if __name__ == "__main__":
  main()
