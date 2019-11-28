# CF Audit Tool

## Features

- utilizes users cf login credentials
- displays search progress
- display result on screen only by default
- option to export results to csv files
- option to scan for routes or service only , default is to scan both
- option to limit search to listed organization(s) and/or space(s)
- option to limit search for listed service(s)
- option to limit search for listed service plan(s)
- option to exclude listed service plan(s)

### Note

You must first login to cloud foundry account on CLI using `cf login` to be able to use this script

### Example Usage

- help message

```bash
./main.py --help
```

- search all organization and spaces you have access to

```bash
./main.py
```

- search in specific organizations

```bash
./main.py -o dit-services,dit-staging
```

- search specific spaces in organization

```bash
./main.py -o dit-staging -s webops-dev,exopps-dev
```

- search for specific services

```bash
py main.py -o dit-staging -s exopps-dev --service redis --services-only
```

- sarch for specific service plans

```bash
py main.py -o dit-staging -s exopps-dev --service-plans tiny
```

- exclude searched service plan

```bash
py main.py -o dit-staging -s exopps-dev --service-plans ha --exclude-services-plans --services-only
```

- exclude service plan for specific service

```bash
py main.py -o dit-staging -s exopps-dev --service redis --service-plans ha --exclude-services-plans --services-only
```

- search for routes only and, export to csv

```bash
./main.py --routes-only --export-csv
```

```bash
./main.py -o dit-staging --routes-ony --export-csv
```

```bash
./main.py -o dit-staging -routes-only --export-csv --quiet
```

- search for services only

```bash
./main.py --services-only
```

### Known Bugs

- script would hang with error , if you have not logged into cf login already , should be fixed for graceful exit after error

### Todo

- option to limit search for listed service(s)
- option to limit search for listed service plan(s)
- option to exclude listed organizations(s),spaces(s),services(s),service plan
