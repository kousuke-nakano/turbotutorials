README.md
--------------------------------------
This document includes TurboRVB, TurboGenius, and TurboWorkflows tutorials.

This document is composed by Sphinx, which is a documentation generator. i.e, it takes a bunch of source files in plain text, and generates a bunch of other awesome things, mainly HTML. For our use case, you can think of it as a program that takes in plain text files in ``reStructuredText`` format, and outputs HTML::

    reStructuredText -> Sphinx -> HTML

Only reStructuredText files are distributed. Indeed, you should generate the HTML documents by yourself.

To generate the documents, first you should install the sphinx module using pip module::

    pip install Sphinx
    pip install sphinx_rtd_theme

The document can be built just by typing::

    make html
    or
    make pdflatex
    
in the root directory (i.e., turborvb_userguides/). The generated documents are::

     html version : turbotutorials -> build -> html -> index.html
     latex-pdf version : turbotutorials -> build -> latex -> index.html

The latex-pdf version is automatically converted from the html files using sphinx. So, please update the source/_sources/.../***.rst files even if you want to edit the pdf one.
   
Enjoy TurboRVB :-)

Kosuke Nakano

