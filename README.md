
  # pip-tree 

  ![](https://img.shields.io/badge/version-0.1.0-gray)
  ![](https://img.shields.io/badge/python-3.10-blue)
  ![](https://img.shields.io/github/license/tikubonn/pip-tree)

pip-tree はインストール済みパッケージの依存関係を抽出するコマンドを追加します。
パッケージの依存関係を抽出するには `pip-tree` コマンドを実行します。

```cmd
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

```cmd
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

```cmd
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

```cmd
pip-tree requests --json
```

```txt
[
  {
    "Name": "requests",
    "Version": "2.28.1",
    "Summary": "Python HTTP for Humans.",
    "Home-page": "https://requests.readthedocs.io",
    "Author": "Kenneth Reitz",
    "Author-email": "me@kennethreitz.org",
    "License": "Apache 2.0",
    "Location": "c:\\users\\tikubonn\\appdata\\local\\programs\\python\\python310\\lib\\site-packages",
    "Requires": [
      "certifi",
      "charset-normalizer",
      "idna",
      "urllib3"
    ],
    "Required-by": [
      "pip-license-gen"
    ],
    "Dependencies": [
      {
        "Name": "certifi",
        "Version": "2022.6.15",
        "Summary": "Python package for providing Mozilla's CA Bundle.",
        "Home-page": "https://github.com/certifi/python-certifi",
        "Author": "Kenneth Reitz",
        "Author-email": "me@kennethreitz.com",
        "License": "MPL-2.0",
        "Location": "c:\\users\\tikubonn\\appdata\\local\\programs\\python\\python310\\lib\\site-packages",
        "Required-by": [
          "pipenv",
          "requests"
        ]
      },
//...
```

`--dump-root-only` オプションを指定することで親パッケージの依存関係だけを抽出できるようになりました。

```cmd
pip-tree --dump-root-only
```

```txt
exolib==0.11.0
  - exofile==0.11.0
pip-license-gen==0.1.0
  - pip-tree==0.1.0
  - requests==2.28.1
    - certifi==2022.6.15
    - charset-normalizer==2.1.0
    - idna==3.3
    - urllib3==1.26.10
pip-licenses==3.5.4
  - PTable==0.9.2
pipenv==2022.7.4
  - certifi==2022.6.15
  - pip==22.1.2
  - setuptools==58.1.0
...
```

その他、細かい部分に関しては `pip-tree -h` コマンドをご参照ください。

```cmd
pip-tree -h
```

## Install

```cmd
python setup.py install
```

## License 

The MIT License.
