#!/bin/bash

for f in *.json; do
  cat $f | jq .rec_texts > $f.md
done

#cat document_0_res.json | jq .rec_texts
