#! /bin/sh
# install.sh - installer for unix

echo Checking for dependencies...

PYTHON=`which python`
if [ $PYTHON ]; then
echo "python found at: $PYTHON"
else
echo "python not found!"
echo "try manual installation by 'python setup.py install'"
exit 1
fi

echo
echo Changing to root to install files

su -c "mkdir ~/.wesen/sources && cp wesen.1.gz /usr/man/man1 && python setup.py install"

echo
echo "put your sources in ~/.wesen/sources/"
echo "Type 'wesen' to run it."