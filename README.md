README.md
--------------------------------------

<img src="logo/turborvb_logo.png" width="70%">

![license](https://img.shields.io/github/license/kousuke-nakano/turbotutorials) ![release](https://img.shields.io/github/release/kousuke-nakano/turbotutorials/all.svg) ![fork](https://img.shields.io/github/forks/kousuke-nakano/turbotutorials?style=social) ![stars](https://img.shields.io/github/stars/kousuke-nakano/turbotutorials?style=social)

This document includes ``TurboRVB``, ``TurboGenius``, and ``TurboWorkflows`` tutorials. Only reStructuredText files are distributed. Indeed, you should generate the HTML documents by yourself using `sphinx`. To generate the documents, first you should install the `sphinx` using pip module::

    pip install sphinx
    pip install sphinx_rtd_theme

The document can be built just by typing::

    make html
    or
    make pdflatex
    
in the root directory (i.e., turborvb_userguides/). The generated documents are::

     html version : turbotutorials -> build -> html -> index.html
     latex-pdf version : turbotutorials -> build -> latex -> index.html

The latex-pdf version is automatically converted from the html files using sphinx. So, please update the ``source/_sources/.../***.rst`` files even if you want to edit the pdf one.
   
Enjoy :-)

Kosuke Nakano

