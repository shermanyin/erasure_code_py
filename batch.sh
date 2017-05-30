#!/usr/bin/env bash

for k in {2..16}; do
    for m in {1..4}; do
        ./a.out $k $m
    done
done
