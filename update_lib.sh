#! /bin/bash

cd Cacheback
source env/bin/activate

python setup.py bdist_wheel
printf "ashishp16" | twine upload dist/*
