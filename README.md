# Benchmarking GNES on Network Latency

<a href="https://drone.gnes.ai/gnes-ai/gnes"><img src="https://drone.gnes.ai/api/badges/gnes-ai/gnes/status.svg" /></a>

This repository tracks the network latency over different GNES versions. As a part of CICD pipeline, this repo gets automatically updated when the [GNES master](https://github.com/gnes-ai/gnes) is updated or a new [GNES version is released](https://github.com/gnes-ai/gnes/releases). 

Please don't change the content of this file manually, as it will be overwritten during the update anyway. 


## Experimental Setup

In this benchmark, we setup multiple workflows to represent typical pipelines in the everyday usage of GNES. We then do a "load testing" to determine the system's behavior under normal/peak conditions.

All experiments use `gnes/gnes:{version}-alpine` as the base image. All microservices are simplified using `BaseRouter` and `BlockRouter`.  

## Run Test

For example, to run the [third test case](#case-3-parallel-non-blocking-flow) on GNES version `latest-alpine`:  

```bash
export GNES_IMG_TAG=latest-alpine
export GNES_BENCHMARK_ID=3

make pull && make build && make test d=1000 b=10 s=1000000 && make clean
```

The client will generate 1000 documents with the batch size of 10, which yields 100 requests in total. Each document has the size of 1MB. Hence each request is 10MB.

## Explanation of the Table

Time units are in *seconds*, *the smaller the better*. Numbers are *the best average* over three runs.

### Time-related metrics

- `roundtrip`: the average latency in seconds for a request travel from `Frontend` and through the whole workflow and finally back to `Frontend`.
- `MB/s`: megabyte per second (MB/s) is a unit of data transfer rate over the whole workflow.
- `f:send`: the average latency in seconds between sending every two requests at the `Frontend`.
- `f:recv`: the average latency in seconds between receiving every two requests at the `Frontend`.
- `f->r1:send`: the average latency in seconds for `Router1` receiving a request sent from `Frontend`.
- `r1->r2:send`: the average latency in seconds for `Router2` receiving a request sent from `Router1` (or all `Router1` from the last layer).
- `r2->f:send`: the average latency in seconds for `Frontend` receiving a request sent from `Router2` (or all `Router2` from the last layer).

### Meta information

- `version_vcs`: corresponds to the `gnes-ai/gnes@` commit's SHA hash.
- `version_tag`: corresponds to the version tag of a GNES docker image.
- `timestamp_build`: timestamp when the docker image was built.
- `timestamp_eval`: timestamp when the benchmark was evaluated.

Table results are sorted by `timestamp_build` with the most recent build at first. 

## Case 1: Non-blocking Flow

The workflow is as follows:

<p align="center">
<a href="https://gnes.ai">
<img src=".github/mermaid-diagram-20190926170713.svg" alt="workflow 1 in test" width=50%>
</a>
</p>

The ideal roundtrip latency is `0`. The smaller the better.

### Result

<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>version_vcs</th>
      <th>roundtrip</th>
      <th>MB/s</th>
      <th>f:send</th>
      <th>f:recv</th>
      <th>f->r1:send</th>
      <th>r1->r2:send</th>
      <th>r2->f:send</th>
      <th>timestamp_build</th>
      <th>timestamp_eval</th>
      <th>version_tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/fda7f96"><code>fda7f96</code></a></td>
      <td>0.286</td>
      <td>3564</td>
      <td>0.120</td>
      <td>0.120</td>
      <td>0.057</td>
      <td>0.052</td>
      <td>0.170</td>
      <td>2019-09-26 11:17:55</td>
      <td>2019-09-27 06:48:53.675573</td>
      <td><code>latest-alpine</code></td>
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

It simulates a pipeline with uneven workload, `Router2` block the pipeline for 1s.

Hence, a naive synchronized pipeline will take 100s to finish 100 requests.

### Result

<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>version_vcs</th>
      <th>roundtrip</th>
      <th>MB/s</th>
      <th>f:send</th>
      <th>f:recv</th>
      <th>f->r1:send</th>
      <th>r1->r2:send</th>
      <th>r2->f:send</th>
      <th>timestamp_build</th>
      <th>timestamp_eval</th>
      <th>version_tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/fda7f96"><code>fda7f96</code></a></td>
      <td>47.862</td>
      <td>50</td>
      <td>0.081</td>
      <td>1.030</td>
      <td>0.050</td>
      <td>46.735</td>
      <td>0.055</td>
      <td>2019-09-26 11:17:55</td>
      <td>2019-09-27 06:55:03.987385</td>
      <td><code>latest-alpine</code></td>
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

The ideal roundtrip latency is `0`. The smaller the better.

### Result

<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>version_vcs</th>
      <th>roundtrip</th>
      <th>MB/s</th>
      <th>f:send</th>
      <th>f:recv</th>
      <th>f->r1:send</th>
      <th>r1->r2:send</th>
      <th>r2->f:send</th>
      <th>timestamp_build</th>
      <th>timestamp_eval</th>
      <th>version_tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/51837cf"><code>51837cf</code></a></td>
      <td>0.275</td>
      <td>3745</td>
      <td>0.119</td>
      <td>0.119</td>
      <td>0.053</td>
      <td>0.044</td>
      <td>0.169</td>
      <td>2019-09-27 06:36:57</td>
      <td>2019-09-27 06:58:13.617126</td>
      <td><code>latest-alpine</code></td>
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

It simulates a parallel pipeline with heavy workload. Both `Router1` and `Router2` will block the pipeline for 1s.

As `Router1` and `Router2` are parallel, a naive synchronized implementation will take 50s to finish 100 requests.

### Result

<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>version_vcs</th>
      <th>roundtrip</th>
      <th>MB/s</th>
      <th>f:send</th>
      <th>f:recv</th>
      <th>f->r1:send</th>
      <th>r1->r2:send</th>
      <th>r2->f:send</th>
      <th>timestamp_build</th>
      <th>timestamp_eval</th>
      <th>version_tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/51837cf"><code>51837cf</code></a></td>
      <td>22.166</td>
      <td>90</td>
      <td>0.061</td>
      <td>0.522</td>
      <td>21.040</td>
      <td>0.058</td>
      <td>0.057</td>
      <td>2019-09-27 06:36:57</td>
      <td>2019-09-27 07:02:55.439558</td>
      <td><code>latest-alpine</code></td>
    </tr>
  </tbody>
</table>