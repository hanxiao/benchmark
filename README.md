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



## Case 1: Unblocking Flow

The workflow is as follows:

<p align="center">
<a href="https://gnes.ai">
<img src=".github/mermaid-diagram-20190926170713.svg" alt="workflow 1 in test">
</a>
</p>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>roundtrip</th>
      <th>f:send interval</th>
      <th>f:recv interval</th>
      <th>f-&gt;r1 trans</th>
      <th>r1-&gt;r2 trans</th>
      <th>r2-&gt;f trans</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th>version</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-09-26 09:44:49.941833</th>
      <th>latest-alpine</th>
      <td>0.296</td>
      <td>0.119</td>
      <td>0.117</td>
      <td>0.052</td>
      <td>0.050</td>
      <td>0.177</td>
    </tr>
    <tr>
      <th>2019-09-26 09:46:13.606679</th>
      <th>latest-alpine</th>
      <td>0.260</td>
      <td>0.116</td>
      <td>0.116</td>
      <td>0.054</td>
      <td>0.049</td>
      <td>0.151</td>
    </tr>
  </tbody>
</table>

## Case 2: Blocking Flow

The workflow is as follows:

<p align="center">
<a href="https://gnes.ai">
<img src=".github/mermaid-diagram-20190926175311.svg" alt="workflow 2 in test">
</a>
</p>

It simulates a pipeline with uneven workload.



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>roundtrip</th>
      <th>f:send interval</th>
      <th>f:recv interval</th>
      <th>f-&gt;r1 trans</th>
      <th>r1-&gt;r2 trans</th>
      <th>r2-&gt;f trans</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th>version</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-09-26 09:52:32.935686</th>
      <th>latest-alpine</th>
      <td>24.708</td>
      <td>0.072</td>
      <td>1.037</td>
      <td>0.040</td>
      <td>23.194</td>
      <td>0.045</td>
    </tr>
  </tbody>
</table>

## Case 3: Parallel Unblocking Flow

The workflow is as follows:

<p align="center">
<a href="https://gnes.ai">
<img src=".github/mermaid-diagram-20190926175843.svg" alt="workflow 3 in test">
</a>
</p>




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>roundtrip</th>
      <th>f:send interval</th>
      <th>f:recv interval</th>
      <th>f-&gt;r1 trans</th>
      <th>r1-&gt;r2 trans</th>
      <th>r2-&gt;f trans</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th>version</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-09-26 10:06:10.805672</th>
      <th>latest-alpine</th>
      <td>0.341</td>
      <td>0.151</td>
      <td>0.145</td>
      <td>0.067</td>
      <td>0.058</td>
      <td>0.206</td>
    </tr>
  </tbody>
</table>

## Case 4: Parallel Blocking Flow

The workflow is as follows:

<p align="center">
<a href="https://gnes.ai">
<img src=".github/mermaid-diagram-20190926180109.svg" alt="workflow 3 in test">
</a>
</p>

It simulates a parallel pipeline with heavy workload.


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>roundtrip</th>
      <th>f:send interval</th>
      <th>f:recv interval</th>
      <th>f-&gt;r1 trans</th>
      <th>r1-&gt;r2 trans</th>
      <th>r2-&gt;f trans</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th>version</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-09-26 10:08:59.486160</th>
      <th>latest-alpine</th>
      <td>11.498</td>
      <td>0.063</td>
      <td>0.507</td>
      <td>10.349</td>
      <td>0.037</td>
      <td>0.039</td>
    </tr>
  </tbody>
</table>