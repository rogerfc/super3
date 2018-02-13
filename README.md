# Super3 video catalog and collector

This program aims at providing the tools to collect and catalog
a private collection of videos based on those published on the
Club Super3 (Catalan TV channel for children) web page.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This has been developed and tested on a macOS computer running python3

### Installing

(optional) Create a virtualenv

```bash
$ virtualenv -p python3 ~/.virtualenvs/super3
$ . ~/.virtualenvs/super3/bin/activate(.fish|.csh)
```

Install the dependencies

```bash
(super3) $ pip install -r requirements.txt
```

## Deployment

This runs locally ATM.


## Usage

Foreseen invocation:

create new catalog
```
$ super3 init
```

add series to catalog with title containing 'Kratt'
```
$ super3 add-series -name 'Kratt'
```

update available episodes
```
$ super3 update
```

list available episodes
```
$ super3 list -name 'Kratt'
```

download available
```
$ super3 download -name 'Kratt'
```


## Built With

* [Requests](http://docs.python-requests.org) - Used to make http calls
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup) - HTTP parser
* [SQLAlchemy](https://www.sqlalchemy.org) - DB ORM

## Contributing

Feel free to contribute

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Roger Firpo** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
