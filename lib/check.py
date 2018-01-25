import json
import sys
from urllib.request import urlopen
from distutils.version import LooseVersion
from typing import Optional, List, Dict


def check(package_name: str, existing_version: Optional[Dict[str, str]]) -> List[Dict[str, str]]:
    url = "https://pypi.python.org/pypi/%s/json" % package_name
    data = json.load(urlopen(url))
    found_versions = list(data["releases"].keys())
    found_versions.sort(key=LooseVersion, reverse=True)

    if existing_version is not None and \
                    existing_version.get("version") is not None:
        existing = LooseVersion(existing_version["version"])
        newer_versions = [v for v in found_versions if LooseVersion(v) >= existing]
    else:
        newer_versions = [found_versions[0]]

    return _wrap(newer_versions)


def main():
    source = json.load(sys.stdin)
    print(json.dumps(check(
        package_name=source['source']['package'],
        existing_version=source.get('version')
    )))


def _wrap(versions: List[str]) -> List[Dict[str, str]]:
    return [{"version": v} for v in versions]
