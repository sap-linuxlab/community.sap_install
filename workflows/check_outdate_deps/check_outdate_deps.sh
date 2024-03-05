#!/usr/bin/env bash

pip3 install -r "$REQUIREMENT_FILE"
input=$(pip3 list --outdated)

compare_versions() {
   local version1=$1 
   local version2=$2
   local IFS='.'

   read -ra version1_splitted <<< "$version1"
   read -ra version2_splitted <<< "$version2"

   for ((i=0;i<${#version1_splitted[@]};i++)); do
       delta=$(( version1_splitted[i] - version2_splitted[i] ))
       if (( delta != 0 )); then
           echo $delta
           return
       fi
   done
   echo 0
}

while read -r line; do
    if [[ $line =~ ^([a-zA-Z0-9-]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([a-zA-Z]+) ]]; then
        package="${BASH_REMATCH[1]}"
        version="${BASH_REMATCH[2]}"
        latest="${BASH_REMATCH[3]}"
        
        if [ "$(compare_versions "$version" "$latest")" -lt 0 ]; then
            ./workflows/check_outdate_deps/open_issue.py "$package" "$version" "$latest"
        fi
    fi
done <<< "$input"
