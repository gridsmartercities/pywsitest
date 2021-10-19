#!/bin/bash
major_max=0;
minor_max=0;
version=$(awk -F'[ ="]+' '$1 == "version" { print $2 }' pyproject.toml)
version=$(echo v$version)
#echo $version
#GITHUB_REPO=pywsitest/tree/automate-test
git tag "${version}"
git log origin/master
echo $(git remote -v)
git remote set-url origin "git@github.com:gridsmartercities/pywsitest.git"
echo $(git remote -v)
git push origin automate-test "${version}" --dry-run
#git push origin "${version}" --dry run
exit 0