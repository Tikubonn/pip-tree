
# pip-tree

## Overview

![](https://img.shields.io/badge/Python-3.12-blue)
![](https://img.shields.io/badge/License-AGPLv3-blue)

pip-tree はインストール済みパッケージの依存関係を抽出するコマンドを追加します。

## Usage

パッケージの依存関係を抽出するには `pip-tree` コマンドを実行します。

```shell
pip-tree
```

```txt
certifi==2022.6.15
charset-normalizer==2.1.0
distlib==0.3.4
filelock==3.7.1
idna==3.3
pip-license-gen==0.1.0
  - pip-tree==0.1.0
  - requests==2.28.1
    - certifi==2022.6.15
    - charset-normalizer==2.1.0
    - idna==3.3
    - urllib3==1.26.10
pip-licenses==3.5.4
  - PTable==0.9.2
pip-tree==0.1.0
...
```

抽出するパッケージを指定することもできます（複数選択も可）。
パッケージが未指定ならばインストールされたすべてのパッケージが検索されます。

```shell
pip-tree requests
```

```txt
requests==2.28.1
  - certifi==2022.6.15
  - charset-normalizer==2.1.0
  - idna==3.3
  - urllib3==1.26.10
```

pipenv にも対応しています。
`pipenv shell` もしくは `pipenv run` とともに使用することで pipenv 環境を参照するようになります。

```shell
pipenv run pip-tree 
```

```txt
aggdraw==1.3.15
attrs==21.4.0
certifi==2022.6.15
charset-normalizer==2.1.0
docopt==0.6.2
exofile==0.11.0
exolib==0.11.0
  - exofile==0.11.0
idna==3.3
imageio==2.19.3
  - numpy==1.23.0
  - Pillow==9.2.0
json5==0.9.8
networkx==2.8.4
Nuitka==0.9.3
...
```

JSON形式にも対応しています。
抽出した依存関係を後であれこれするときに便利です。

```shell
pip-tree requests --json
```

```txt
[
  {
    "metadata_version": "2.4",
    "name": "requests",
    "version": "2.32.5",
    "summary": "Python HTTP for Humans.",
    "home_page": "https://requests.readthedocs.io",
    "author": "Kenneth Reitz",
    "author_email": "me@kennethreitz.org",
    "license": "Apache-2.0",
    "project_url": [
      "Documentation, https://requests.readthedocs.io",
      "Source, https://github.com/psf/requests"
    ],
    "classifier": [
      "Development Status :: 5 - Production/Stable",
      "Environment :: Web Environment",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: Apache Software License",
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3.11",
      "Programming Language :: Python :: 3.12",
      "Programming Language :: Python :: 3.13",
      "Programming Language :: Python :: 3.14",
      "Programming Language :: Python :: 3 :: Only",
      "Programming Language :: Python :: Implementation :: CPython",
      "Programming Language :: Python :: Implementation :: PyPy",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Software Development :: Libraries"
    ],
    "requires_python": ">=3.9",
    "description_content_type": "text/markdown",
    "license_file": "LICENSE",
    "requires_dist": [
      "charset_normalizer<4,>=2",
      "idna<4,>=2.5",
      "urllib3<3,>=1.21.1",
      "certifi>=2017.4.17",
      "PySocks!=1.5.7,>=1.5.6; extra == \"socks\"",
      "chardet<6,>=3.0.2; extra == \"use-chardet-on-py3\""
    ],
    "provides_extra": [
      "security",
      "socks",
      "use-chardet-on-py3"
    ],
    "dynamic": [
      "author",
      "author-email",
      "classifier",
      "description",
      "description-content-type",
      "home-page",
      "license",
      "license-file",
      "project-url",
      "provides-extra",
      "requires-dist",
      "requires-python",
      "summary"
    ],
    "description": "# Requests\n\n**Requests** is a simple, yet elegant, HTTP library.\n\n```python\n>>> import requests\n>>> r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))\n>>> r.status_code\n200\n>>> r.headers['content-type']\n'application/json; charset=utf8'\n>>> r.encoding\n'utf-8'\n>>> r.text\n'{\"authenticated\": true, ...'\n>>> r.json()\n{'authenticated': True, ...}\n```\n\nRequests allows you to send HTTP/1.1 requests extremely easily. There\u2019s no need to manually add query strings to your URLs, or to form-encode your `PUT` & `POST` data \u2014 but nowadays, just use the `json` method!\n\nRequests is one of the most downloaded Python packages today, pulling in around `30M downloads / week`\u2014 according to GitHub, Requests is currently [depended upon](https://github.com/psf/requests/network/dependents?package_id=UGFja2FnZS01NzA4OTExNg%3D%3D) by `1,000,000+` repositories. You may certainly put your trust in this code.\n\n[![Downloads](https://static.pepy.tech/badge/requests/month)](https://pepy.tech/project/requests)\n[![Supported Versions](https://img.shields.io/pypi/pyversions/requests.svg)](https://pypi.org/project/requests)\n[![Contributors](https://img.shields.io/github/contributors/psf/requests.svg)](https://github.com/psf/requests/graphs/contributors)\n\n## Installing Requests and Supported Versions\n\nRequests is available on PyPI:\n\n```console\n$ python -m pip install requests\n```\n\nRequests officially supports Python 3.9+.\n\n## Supported Features & Best\u2013Practices\n\nRequests is ready for the demands of building robust and reliable HTTP\u2013speaking applications, for the needs of today.\n\n- Keep-Alive & Connection Pooling\n- International Domains and URLs\n- Sessions with Cookie Persistence\n- Browser-style TLS/SSL Verification\n- Basic & Digest Authentication\n- Familiar `dict`\u2013like Cookies\n- Automatic Content Decompression and Decoding\n- Multi-part File Uploads\n- SOCKS Proxy Support\n- Connection Timeouts\n- Streaming Downloads\n- Automatic honoring of `.netrc`\n- Chunked HTTP Requests\n\n## API Reference and User Guide available on [Read the Docs](https://requests.readthedocs.io)\n\n[![Read the Docs](https://raw.githubusercontent.com/psf/requests/main/ext/ss.png)](https://requests.readthedocs.io)\n\n## Cloning the repository\n\nWhen cloning the Requests repository, you may need to add the `-c\nfetch.fsck.badTimezone=ignore` flag to avoid an error about a bad commit timestamp (see\n[this issue](https://github.com/psf/requests/issues/2690) for more background):\n\n```shell\ngit clone -c fetch.fsck.badTimezone=ignore https://github.com/psf/requests.git\n```\n\nYou can also apply this setting to your global Git config:\n\n```shell\ngit config --global fetch.fsck.badTimezone ignore\n```\n\n---\n\n[![Kenneth Reitz](https://raw.githubusercontent.com/psf/requests/main/ext/kr.png)](https://kennethreitz.org) [![Python Software Foundation](https://raw.githubusercontent.com/psf/requests/main/ext/psf.png)](https://www.python.org/psf)\n",
    "_dependencies": [
      {
        "metadata_version": "2.4",
        "name": "certifi",
        "version": "2026.1.4",
        "summary": "Python package for providing Mozilla's CA Bundle.",
        "home_page": "https://github.com/certifi/python-certifi",
        "author": "Kenneth Reitz",
        "author_email": "me@kennethreitz.com",
        "license": "MPL-2.0",
        "project_url": [
          "Source, https://github.com/certifi/python-certifi"
        ],
        "classifier": [
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
          "Natural Language :: English",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: 3.13",
          "Programming Language :: Python :: 3.14"
        ],
...
```

その他、細かい部分に関しては `pip-tree -h` コマンドをご参照ください。

```shell
pip-tree -h
```

## Install

```shell
pip install .
```

## Donation

<a href="https://buymeacoffee.com/tikubonn" target="_blank"><img src="doc/img/qr-code.png" width="3000px" height="3000px" style="width:150px;height:auto;"></a>

もし本パッケージがお役立ちになりましたら、少額の寄付で支援することができます。<br>
寄付していただいたお金は書籍の購入費用や日々の支払いに使わせていただきます。
ただし、これは寄付の多寡によって継続的な開発やサポートを保証するものではありません。ご留意ください。

If you found this package useful, you can support it with a small donation.
Donations will be used to cover book purchases and daily expenses.
However, please note that this does not guarantee ongoing development or support based on the amount donated.

## License

© 2022-2026 tikubonn

[pip-tree](https://github.com/tikubonn/pip-tree) licensed under the [AGPLv3](./LICENSE).
