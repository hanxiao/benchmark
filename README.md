# Benchmarking GNES on Network Latency

This repository tracks the network latency of different GNES versions. It gets updated when the [GNES master](https://github.com/gnes-ai/gnes) is updated or a new [GNES version is released](https://github.com/gnes-ai/gnes/releases). 

Please don't change the content of this file manually, as it will be overwritten during the update anyway. 

## Run Test

For example, to run the [third test case](#case-3-parallel-non-blocking-flow) on GNES version `latest-alpine`:  

```bash
export GNES_IMG_TAG=latest-alpine
export GNES_BENCHMARK_ID=3

make pull && make build && make test d=500 b=10 s=1000000 && make clean
```

The client will generate 500 documents and send them in 10 batches, each document has the size of 1MB. Hence each request is about 50MB.

Units are in millisecond, the smaller the better.

`version_vcs` corresponds to the `gnes-ai/gnes@` commit's SHA hash.

## Case 1: Non-blocking Flow

The workflow is as follows:

<p align="center">
<a href="https://gnes.ai">
<img src=".github/mermaid-diagram-20190926170713.svg" alt="workflow 1 in test" width=50%>
</a>
</p>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>version_vcs</th>
      <th>version_tag</th>
      <th>roundtrip</th>
      <th>f:send interval</th>
      <th>f:recv interval</th>
      <th>f->r1 trans</th>
      <th>r1->r2 trans</th>
      <th>r2->f trans</th>
      <th>timestamp_build</th>
      <th>timestamp_eval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>gnes-ai/gnes@fda7f96</code></td>
      <td><code>latest-alpine</code></td>
      <td>0.250</td>
      <td>0.107</td>
      <td>0.091</td>
      <td>0.056</td>
      <td>0.041</td>
      <td>0.148</td>
      <td>2019-09-26 11:17:55</td>
      <td>2019-09-26 11:37:08.995740</td>
    </tr>
  </tbody>
</table>

## Case 2: Blocking Flow

The workflow is as follows:

<p align="center">
<a href="https://gnes.ai">
<img src=".github/mermaid-diagram-20190926175311.svg" alt="workflow 2 in test" width=50%>
</a>
</p>

It simulates a pipeline with uneven workload.



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>version_vcs</th>
      <th>version_tag</th>
      <th>roundtrip</th>
      <th>f:send interval</th>
      <th>f:recv interval</th>
      <th>f->r1 trans</th>
      <th>r1->r2 trans</th>
      <th>r2->f trans</th>
      <th>timestamp_build</th>
      <th>timestamp_eval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>gnes-ai/gnes@fda7f96</code></td>
      <td><code>latest-alpine</code></td>
      <td>24.579</td>
      <td>0.072</td>
      <td>1.028</td>
      <td>0.039</td>
      <td>23.490</td>
      <td>0.040</td>
      <td>2019-09-26 11:17:55</td>
      <td>2019-09-26 11:59:43.815398</td>
    </tr>
  </tbody>
</table>

## Case 3: Parallel Non-blocking Flow

The workflow is as follows:

<p align="center">
<a href="https://gnes.ai">
<img src=".github/mermaid-diagram-20190926175843.svg" alt="workflow 3 in test"  width=50%>
</a>
</p>




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>version_vcs</th>
      <th>version_tag</th>
      <th>roundtrip</th>
      <th>f:send interval</th>
      <th>f:recv interval</th>
      <th>f->r1 trans</th>
      <th>r1->r2 trans</th>
      <th>r2->f trans</th>
      <th>timestamp_build</th>
      <th>timestamp_eval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>gnes-ai/gnes@fda7f96</code></td>
      <td><code>latest-alpine</code></td>
      <td>0.281</td>
      <td>0.121</td>
      <td>0.119</td>
      <td>0.057</td>
      <td>0.045</td>
      <td>0.173</td>
      <td>2019-09-26 11:17:55</td>
      <td>2019-09-26 12:01:11.401479</td>
    </tr>
  </tbody>
</table>

## Case 4: Parallel Blocking Flow

The workflow is as follows:

<p align="center">
<a href="https://gnes.ai">
<img src=".github/mermaid-diagram-20190926180109.svg" alt="workflow 4 in test"  width=50%>
</a>
</p>

It simulates a parallel pipeline with heavy workload.


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>version_vcs</th>
      <th>version_tag</th>
      <th>roundtrip</th>
      <th>f:send interval</th>
      <th>f:recv interval</th>
      <th>f->r1 trans</th>
      <th>r1->r2 trans</th>
      <th>r2->f trans</th>
      <th>timestamp_build</th>
      <th>timestamp_eval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>gnes-ai/gnes@fda7f96</code></td>
      <td><code>latest-alpine</code></td>
      <td>11.007</td>
      <td>0.070</td>
      <td>0.506</td>
      <td>9.856</td>
      <td>0.037</td>
      <td>0.041</td>
      <td>2019-09-26 11:17:55</td>
      <td>2019-09-26 12:03:37.293088</td>
    </tr>
  </tbody>
</table>