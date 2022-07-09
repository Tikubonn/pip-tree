
import re 
import os 
import sys 
import json 
import subprocess 
from pathlib import Path 
from argparse import ArgumentParser

def open_output_file (path, *args, **kwargs):
  if path:
    return open(path, *args, **kwargs)
  else:
    fd = os.dup(sys.stdout.fileno())
    return os.fdopen(fd, *args, **kwargs)

def list_pip_installed ():
  packages = list()
  process = subprocess.run(["pip", "freeze"], shell=True, text=True, stdout=subprocess.PIPE, check=True)
  for line in process.stdout.strip().split("\n"):
    matchresult = re.match(r"^(\S+?)==\S+$", line)
    if matchresult:
      name, = matchresult.groups()
      packages.append(name)
      continue
    matchresult = re.match(r"^(\S+?) @ .*$", line)
    if matchresult:
      name, = matchresult.groups()
      packages.append(name)
      continue
    matchresult = re.match(r"^# Editable install with no version control \((\S+?)==.*$", line)
    if matchresult:
      name, = matchresult.groups()
      packages.append(name)
      continue
  return packages

def get_pip_info (package):
  packageinfo = dict()
  process = subprocess.run(["pip", "show", package], shell=True, text=True, stdout=subprocess.PIPE, check=True)
  for line in process.stdout.strip().split("\n"):
    matchresult = re.match(r"(.*?):(.*)", line)
    if matchresult:
      key, value = matchresult.groups()
      if value.strip():
        if key.strip() == "Requires":
          packageinfo[key.strip()] = [val.strip() for val in value.split(",")]
        elif key.strip() == "Required-by":
          packageinfo[key.strip()] = [val.strip() for val in value.split(",")]
        else:
          packageinfo[key.strip()] = value.strip()
  return packageinfo

def get_pip_info_tree (packages):
  packageinfos = list()
  packageinfotable = dict()
  for package in packages:
    if package not in packageinfotable:
      packageinfotable[package] = get_pip_info(package)
    packageinfo = packageinfotable[package]
    packageinfos.append(packageinfo)
  packageinfostack = packageinfos.copy()
  while packageinfostack:
    packageinfo = packageinfostack.pop()
    if "Dependencies" not in packageinfo:
      for pkg in packageinfo.get("Requires", []):
        if pkg not in packageinfotable:
          packageinfotable[pkg] = get_pip_info(pkg)
        pkginfo = packageinfotable[pkg]
        packageinfo.setdefault("Dependencies", [])
        packageinfo["Dependencies"].append(pkginfo)
        packageinfostack.append(pkginfo)
  return packageinfos

def dump_pip_info_tree (packageinfos, *, _depth=0, indent=2, file=sys.stdout):
  for packageinfo in packageinfos:
    if _depth:
      print("{:s}- {:s}=={:s}".format(" " * _depth, packageinfo["Name"], packageinfo["Version"]), file=file)
    else:
      print("{:s}=={:s}".format(packageinfo["Name"], packageinfo["Version"]), file=file)
    dump_pip_info_tree(packageinfo.get("Dependencies", []), _depth=_depth + indent, indent=indent, file=file)

def main ():
  parser = ArgumentParser(description="Dump installed package info by pip.")
  parser.add_argument("packages", nargs="*", help="Package names for dump.")
  parser.add_argument("--json", action="store_true", help="Dump information as JSON format.")
  parser.add_argument("--indent", nargs="?", default=2, help="Amount of indentation depth.")
  parser.add_argument("--dump-root-only", action="store_true", help="If enabled, show root packages only.")
  parser.add_argument("-o", "--output-file", type=Path, help="Path of output file. (default is stdout).")
  parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")
  args = parser.parse_args()
  if args.packages:
    packages = args.packages
  else:
    packages = list_pip_installed()
  packageinfos = get_pip_info_tree(packages)
  if args.dump_root_only: #--dump-root-onlyが真ならば親をもたないパッケージのみ抽出する。
    packageinfos = [packageinfo for packageinfo in packageinfos if not packageinfo.get("Required-by", [])]
  with open_output_file(args.output_file, "w", encoding="utf-8") as stream:
    if args.json:
      json.dump(packageinfos, stream, indent=args.indent)
    else:
      dump_pip_info_tree(packageinfos, file=stream, indent=args.indent)

if __name__ == "__main__":
  main()
