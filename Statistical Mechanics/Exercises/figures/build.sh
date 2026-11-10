#!/usr/bin/env bash
# Rebuild every figure PDF in this folder from its standalone .tex source.
# Usage: ./build.sh            (all figures)
#        ./build.sh gallery    (one figure, by name without .tex)
# To regenerate the computed diagrams first:
#   python3 make_gallery.py  > binary_gallery.tex
#   python3 make_pressure.py > binary_pressure.tex
set -e
cd "$(dirname "$0")"
figs="${@:-$(grep -l 'documentclass\[11pt,tikz' *.tex | sed 's/\.tex$//')}"
for f in $figs; do
    pdflatex -interaction=nonstopmode -halt-on-error "$f.tex" > /dev/null
    echo "built $f.pdf"
done
rm -f *.aux *.log
