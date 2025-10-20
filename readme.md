# cnf

load config files and create them if they don't exist.

```
config = cnf.makeload(".myprog/conf", root=cnf.home, fmt="yaml", make=template)
```

documentation [here](https://numlims.github.io/cnf/).

## install

download cnf whl from
[here](https://github.com/numlims/cnf/releases). install whl with
pip:

```
pip install dbcq-<version>.whl
```

## dev

edit [`cnf/init.ct`](./cnf/init.ct).

to generate the code from the .ct files get [ct](https://github.com/tnustrings/ct).

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
