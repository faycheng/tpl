#!/usr/bin/env bash


export_alias(){
    builtin export 'TPL_'$@
}

alias export=export_alias