#!/usr/bin/env bash

file_name="echo"
message="hellp tpl"

echo "{\"file_name\":\"$file_name\", \"message\":\"$message\"}" >> $pipe

