# Benchmarking GNES on Network Latency

This repository tracks the network latency of different GNES versions. It gets updated when the [GNES master](https://github.com/gnes-ai/gnes) is updated or a new [GNES version is released](https://github.com/gnes-ai/gnes/releases). 

Please don't write the content of this file manually, as it will be overrided during the update anyway. 

## Run Test

For example, to run the third test case on GNES version `latest-alpine`:  

```bash
export GNES_IMG_TAG=latest-alpine
export GNES_BENCHMARK_ID=3

make pull && make build && make test d=500 b=10 s=1000000 && make clean
```

The client will generate 500 documents and send them in 10 batches, each document has the size of 1MB. Hence each request is about 50MB.

