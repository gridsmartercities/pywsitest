#!/bin/bash

set -eu

git config --global user.name Miriam
git config --global user.email not.miriam@gird.dev

git clone git@github.com:gridsmartercities/pywsitest.git miriam
git miriam

git tag -a -m "Miriam to the resque" 1.4.8
git push origin 1.4.8


echo "victory"

#major_max=0;
#minor_max=0;
#version=$(awk -F'[ ="]+' '$1 == "version" { print $2 }' pyproject.toml)
#version=$(echo v$version)
#echo $version
#GITHUB_REPO=pywsitest/tree/automate-test
#git checkout master
#git tag "${version}"
#git log origin/master
#echo $(git remote -v)
#git remote set-url origin "git@github.com:gridsmartercities/pywsitest.git"
#echo $(git remote -v)
#git push origin master "${version}" --dry-run
#git push origin "${version}" --dry run
#exit 0