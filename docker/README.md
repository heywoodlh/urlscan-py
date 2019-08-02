### Usage:

```
 docker run --rm -i heywoodlh/urlscan-py urlscan [options] ...
```

Get help, for example:

```
 docker run --rm -i heywoodlh/urlscan-py urlscan --help
```

If you want your API/DB config to persist on the host, use something like this:

```
docker run --rm -i -v ~/.urlscan:/root/.urlscan heywoodlh/urlscan-py urlscan [options] ...
```


For more instructions on the usage of the command line tool look at the [README](https://github.com/heywoodlh/urlscan-py/blob/master/README.md).
