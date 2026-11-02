# cnf

load config files and create them if they don't exist.

```
import cnf
mycnf = cnf.cnf("myprog/conf.yaml", roots=[cnf.system, cnf.user], fmt="yaml", make=template)
conf = mycnf.conf
```

documentation [here](https://numlims.github.io/cnf/).

## install

download cnf whl from
[here](https://github.com/numlims/cnf/releases). install whl with
pip:

```
pip install cnf-<version>.whl
```

## dev

edit [`cnf/init.ct`](./cnf/init.ct).

generate the code from the .ct files with [ct](https://github.com/tnustrings/ct).

build and install:

```
make install
```

test:

```
make test
```

generate api doc:

```
make doc
```
