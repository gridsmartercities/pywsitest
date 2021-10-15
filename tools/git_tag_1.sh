#!/bin/bash
major_max=0;
minor_max=0;
version=$(awk -F'[ ="]+' '$1 == "version" { print $2 }' pyproject.toml)
#echo $version
git add -u
git commit -m "${version}"
git tag "${version}"
git push -u origin "${version}"
exit 0