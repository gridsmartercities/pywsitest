#!/bin/bash
major_max=0;
minor_max=0;
version=$(awk -F'[ ="]+' '$1 == "version" { print $2 }' pyproject.toml)
version=$(echo v$version)
#echo $version
git tag "${version}"
git push origin "${version}"
exit 0