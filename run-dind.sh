#!/usr/bin/env bash

cd /workspace

rm -rf benchmark

git clone https://github.com/gnes-ai/benchmark.git

cd benchmark

export GNES_IMG_TAG=latest-alpine

for EXP_ID in 1 2 ;
do
    export GNES_BENCHMARK_ID=$EXP_ID
    make pull && make build && make test d=100 b=10 s=10 && make clean
    make wait t=20
done


#for EXP_ID in 1 2 3 4 ;
#do
#    export GNES_BENCHMARK_ID=$EXP_ID
#    make pull && make build && make test d=1000 b=10 s=1000000 && make clean
#    make wait t=20
#done