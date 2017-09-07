#!/usr/bin/env bash

file_name="echo"
message="hello tpl"

echo "{\"file_name\":\"$file_name\", \"message\":\"$message\"}" >> $pipe

