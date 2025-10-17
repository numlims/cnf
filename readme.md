# cnf - config file handler

load config files and create them if they don't exist.

```
config = cnf.makeload(".myprog/conf", from=cnf.home, fmt="yaml", make=template)
```