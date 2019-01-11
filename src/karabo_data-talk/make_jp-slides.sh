#!/bin/bash
if [ -z "$1" ];then
   echo ""
   echo "No Notebook file given usage:"
   echo "$(basename $0) jupyter_notebook_file.ipynb [output_filename] [browser]"
   echo ""
   exit 257
fi
infile=$1
if [ "$2" ];then
   theme=$2
else
   theme='serif'
fi

export BROWSER=firefox
jupyter nbconvert $infile --to slides \
   --config=$(dirname $0)/slides_config.py \
   --SlidesExporter.reveal_theme=$theme \
   --SlidesExporter.reveal_scroll=True \
   --reveal-prefix=$(dirname $0)/reveal.js
