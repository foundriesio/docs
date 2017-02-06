#!/bin/bash

#server="http://deploy.gitci.com"
#server="http://gitci.com:8080"
server="localhost:8080"
rest="rest/v1"
auth_header="Authorization: Basic YWRtaW46YWRtaW4="
base_url="$server/$rest"

file=$1
version=$2

if [ -z "$file" ] || [ -z "$version" ]; then
	echo "Missing input arguments (file version)"
	exit 1
fi

# Create new distribution set
ret=`curl "$base_url/distributionsets" -s -H "$auth_header" -H 'Content-Type: application/json' -X POST -d "[ {
\"name\" : \"Zephyr RPB\",
\"description\" : \"Zephyr Reference Platform Build\",
\"version\" : \"$version\",
\"requiredMigrationStep\" : false,
\"type\" : \"os\"
} ]"`
dsid=`echo $ret | sed -e 's/.*id":\([0-9]\+\).*/\1/'`

# Create new software module
ret=`curl "$base_url/softwaremodules" -s -H "$auth_header" -H 'Content-Type: application/json' -X POST -d "[ {
\"name\" : \"Zephyr RPB Firmware\",
\"vendor\" : \"Linaro\",
\"description\" : \"Zephyr Reference Platform Build\",
\"version\" : \"$version\",
\"type\" : \"os\"
} ]"`
smid=`echo $ret | sed -e 's/.*id":\([0-9]\+\).*/\1/'`

# Upload artifact
ret=`curl "$base_url/softwaremodules/$smid/artifacts" -s -H "$auth_header" -H 'Content-Type: multipart/form-data' -X POST -F "file=@$file"`

# Assign software module
ret=`curl "$base_url/distributionsets/$dsid/assignedSM" -s -H "$auth_header" -H 'Content-Type: application/json' -X POST -d "[ { \"id\" : \"$smid\" } ]"`

echo "Created DS $dsid, SM $smid and uploaded artifact $file"
