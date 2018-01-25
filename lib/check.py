import json
from urllib.request import urlopen
from distutils.version import LooseVersion
from typing import Optional, List


def check(package_name: str, existing_version: Optional[str]) -> List[str]:
    url = "https://pypi.python.org/pypi/%s/json" % package_name
    data = json.load(urlopen(url))
    versions = list(data["releases"].keys())
    versions.sort(key=LooseVersion, reverse=True)
    if existing_version is not None:
        return [v for v in versions if LooseVersion(v) >= LooseVersion(existing_version)]
    else:
        return versions
