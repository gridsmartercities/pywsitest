#!/bin/bash
major_max=0;
minor_max=0;
patch_max=0;
BRANCH_NAME=automate-test;
ver=${VERSION}
branch_name="${BRANCH_NAME}"
echo "Creating tag for branch $BRANCH_NAME"
if [ -z "$BRANCH_NAME" ]; then
    echo 'BRANCH_NAME not provided'
    exit 1
fi
git checkout $BRANCH_NAME
#git tag -d $(git tag -l)
git fetch --tags
last_tag=$(git tag -l | sort -V | tail -n 1)
if [[ $last_tag ]]; then
    echo "Last tag: $last_tag"
    version=$(echo $last_tag | grep -o '[^-]*$')
    major=$(echo $version | cut -d. -f1)
    minor=$(echo $version | cut -d. -f2)
    patch=$(echo $version | cut -d. -f3)
if [ "$major_max" -lt "$major" ]; then
        let major_max=$major
    fi
if [ "$minor_max" -lt "$minor" ]; then
        let minor_max=$minor
    fi
if [ "$patch_max" -lt "$patch" ]; then
        let patch_max=$patch
    fi
    let patch_max=($patch_max+1)
fi
if [ "$major_max" -ne "${MAJOR_VERSION}" ] || [ "$minor_max" -ne "${MINOR_VERSION}" ]; then
    major_max="${MAJOR_VERSION}"
    minor_max="${MINOR_VERSION}"
fi

echo 'Switching to new version:' $major_max'.'$minor_max'.'$patch_max
$(git tag -a $major_max.$minor_max.$patch_max -m "Version $major_max.$minor_max.$patch_max")
VERSION=$(echo v$major_max.$minor_max.$patch_max)

echo 'Push tag to remote'
#$(git push origin $branch_name-$major_max.$minor_max.$patch_max $branch_name)
exit 0