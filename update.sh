#!/bin/bash
rm -r Downloaded_Files/ # Remove Downloaded_files/
python setup/setup.py bdist_wheel # Run the setup script to rebuild cadtlib
rm setup/cadtlib-0.1.0-py3-none-any.whl # Remove previous installer for cadtlib
mv dist/cadtlib-0.1.0-py3-none-any.whl setup # Move new cadtlib installer to setup/
rm -r dist
rm -r cadtlib.egg-info
rm -r build