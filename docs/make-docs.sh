#!/bin/bash
rm -fr source-code/modules
rm -fr _build
sphinx-apidoc -e -o source-code/modules ./../pyextract/
make html
