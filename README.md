# ews_builder

`ews-builder` takes the Exchange Web Services WSDL files and generates EWS SOAP request bodies for each operation/endpoint.

## Getting Started

To use `ews-builder` you can run it directly.  Since `ews-builder` is mainly considered a command line tool, once installed, you run it directly:

```bash
# Will display the help system
ews-builder

# to build a service type
ews-builder build

# select 'All' or specific services to build
Please select 'All' or specific services to generate

 * All
   FindAvailableMeetingTimes
   FindMeetingTimeCandidates
   UploadItems
   ExportItems
   ConvertId
   GetFolder
   CreateFolder
   CreateFolderPath
   CreateManagedFolder
   DeleteFolder
   ......

# get show additional paramters use the help
ews-builder build --help

INFO: Showing help with the command 'ews-builder build -- --help'.

NAME
    ews-builder build

SYNOPSIS
    ews-builder build <flags>

FLAGS
    --service_name=SERVICE_NAME
    --generate_strings=GENERATE_STRINGS
    --output=OUTPUT
```

### Prerequisites

This package installs the following packages:

```
pyyaml
fire
pick
```

### Installing

In order to use carcass you can install it via `pip` or clone this repository.

```bash
pip install ews-builder
```

```bash
git clone git@github.com:swimlane/ews-builder.git
cd ews-builder
pip install -r requirements.txt
```

## Built With

* [carcass](https://github.com/MSAdministrator/carcass) - Python packaging template

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

* Josh Rickard - *Initial work* - [MSAdministrator](https://github.com/MSAdministrator)

See also the list of [contributors](https://github.com/swimlane/ews-builder/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details
