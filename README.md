# TurboRVB Tutorials

<img src="logo/turborvb_logo.png" width="70%">

![license](https://img.shields.io/github/license/kousuke-nakano/turbotutorials) ![release](https://img.shields.io/github/release/kousuke-nakano/turbotutorials/all.svg) ![fork](https://img.shields.io/github/forks/kousuke-nakano/turbotutorials?style=social) ![stars](https://img.shields.io/github/stars/kousuke-nakano/turbotutorials?style=social)

## Overview

This repository contains comprehensive tutorials for the TurboRVB ecosystem, including:
- TurboRVB: A quantum Monte Carlo package for electronic structure calculations
- TurboGenius: A Python package for automated quantum Monte Carlo calculations
- TurboWorkflows: A workflow management system for high-throughput quantum Monte Carlo calculations

The tutorials are deployed from [GitHub Pages](https://kousuke-nakano.github.io/turbotutorials/).

## Prerequisites

Before building the documentation, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/kousuke-nakano/turbotutorials.git
cd turbotutorials
```

2. Install required Python packages:
```bash
pip install sphinx sphinx_rtd_theme
```

## Building the Documentation

You can build the documentation in two formats:

### HTML Version
```bash
make html
```
The generated HTML files will be available in `build/html/`. Open `build/html/index.html` in your web browser to view the documentation.

### PDF Version
```bash
make pdflatex
```
The generated PDF will be available in `build/latex/`.

## Project Structure

- `source/_sources/`: Contains all the reStructuredText (`.rst`) source files
- `build/`: Contains the generated documentation
  - `html/`: HTML version of the documentation
  - `latex/`: PDF version of the documentation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Note

The PDF version is automatically converted from the HTML files using Sphinx. Therefore, please update the files in `source/_sources/.../***.rst` even if you want to edit the PDF version.

## License

This project is licensed under the terms specified in the LICENSE file.

## Author

Kosuke Nakano

## Acknowledgments

- TurboRVB team for their excellent quantum Monte Carlo package
- Sphinx team for the documentation framework
- All contributors and users of the TurboRVB ecosystem

