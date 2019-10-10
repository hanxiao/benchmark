# Benchmarking GNES on Network Latency

<a href="https://drone.gnes.ai/gnes-ai/gnes"><img src="https://drone.gnes.ai/api/badges/gnes-ai/gnes/status.svg" /></a>

This repository tracks the network latency over different GNES versions. As a part of CICD pipeline, this repo gets automatically updated when the [GNES master](https://github.com/gnes-ai/gnes) is updated or a new [GNES version is released](https://github.com/gnes-ai/gnes/releases). 

Please don't change the content of this file manually, as it will be overwritten during the update anyway. 


## Experimental Setup

In this benchmark, we setup multiple workflows to represent typical pipelines in the everyday usage of GNES. We then do a "load testing" to determine the system's behavior under normal/peak conditions.

All experiments use `gnes/gnes:{version}-alpine` as the base image. All microservices are simplified using `BaseRouter` and `BlockRouter`.  

## Run Test

> For the purpose of evaluating this benchmark in CICD pipeline, some environment 

For example, to run the [third test case](#case-3-parallel-non-blocking-flow) on GNES version `latest-alpine`:  

```bash
export GNES_IMG_TAG=latest-alpine
export GNES_BENCHMARK_ID=3

make pull && make build && make test d=500 b=10 s=1000000 && make clean
```

The client will generate 500 documents with the batch size of 10, which yields 50 requests in total. Each document has the size of 1MB. Hence each request is 10MB.

Due to the memory limit of our CD node (t2-micro, 1GB memory), we better keep the number of document in this way.

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

<p align="center">
<a href="https://gnes.ai">
<img src=".github/data-rate-1.svg" alt="workflow 1 in test" width=60%>
</a>
</p>



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
      <td><a href="https://github.com/gnes-ai/gnes/commit/49150fb"><code>49150fb</code></a></td>
      <td>3.314</td>
      <td>227</td>
      <td>0.123</td>
      <td>0.010</td>
      <td>0.053</td>
      <td>0.046</td>
      <td>3.204</td>
      <td>2019-10-10 04:51</td>
      <td>2019-10-10 05:18</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/17f9287"><code>17f9287</code></a></td>
      <td>0.161</td>
      <td>3148</td>
      <td>0.127</td>
      <td>0.125</td>
      <td>0.032</td>
      <td>0.051</td>
      <td>0.069</td>
      <td>2019-10-10 00:33</td>
      <td>2019-10-10 01:00</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/3aab341"><code>3aab341</code></a></td>
      <td>0.161</td>
      <td>3150</td>
      <td>0.129</td>
      <td>0.127</td>
      <td>0.032</td>
      <td>0.052</td>
      <td>0.068</td>
      <td>2019-10-09 10:15</td>
      <td>2019-10-09 10:39</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/fc546f0"><code>fc546f0</code></a></td>
      <td>0.160</td>
      <td>3166</td>
      <td>0.128</td>
      <td>0.126</td>
      <td>0.032</td>
      <td>0.047</td>
      <td>0.068</td>
      <td>2019-09-30 09:41</td>
      <td>2019-09-30 10:08</td>
      <td><code>v0.0.43-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/83f96d9"><code>83f96d9</code></a></td>
      <td>0.160</td>
      <td>3171</td>
      <td>0.127</td>
      <td>0.126</td>
      <td>0.032</td>
      <td>0.048</td>
      <td>0.068</td>
      <td>2019-09-29 12:34</td>
      <td>2019-09-29 13:01</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/4dcf6d0"><code>4dcf6d0</code></a></td>
      <td>0.159</td>
      <td>3185</td>
      <td>0.127</td>
      <td>0.125</td>
      <td>0.031</td>
      <td>0.050</td>
      <td>0.068</td>
      <td>2019-09-29 11:57</td>
      <td>2019-09-29 12:24</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/0bb0082"><code>0bb0082</code></a></td>
      <td>0.160</td>
      <td>3172</td>
      <td>0.128</td>
      <td>0.126</td>
      <td>0.031</td>
      <td>0.048</td>
      <td>0.068</td>
      <td>2019-09-29 11:23</td>
      <td>2019-09-29 11:47</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/cb4e46a"><code>cb4e46a</code></a></td>
      <td>0.159</td>
      <td>3182</td>
      <td>0.127</td>
      <td>0.126</td>
      <td>0.031</td>
      <td>0.047</td>
      <td>0.068</td>
      <td>2019-09-29 04:07</td>
      <td>2019-09-29 04:34</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/a087626"><code>a087626</code></a></td>
      <td>2.534</td>
      <td>727</td>
      <td>1.114</td>
      <td>1.052</td>
      <td>0.537</td>
      <td>0.478</td>
      <td>1.491</td>
      <td>2019-09-27 11:05</td>
      <td>2019-09-27 11:35</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/51837cf"><code>51837cf</code></a></td>
      <td>0.155</td>
      <td>3258</td>
      <td>0.124</td>
      <td>0.123</td>
      <td>0.032</td>
      <td>0.047</td>
      <td>0.064</td>
      <td>2019-09-27 06:36</td>
      <td>2019-09-27 10:29</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/51837cf"><code>51837cf</code></a></td>
      <td>0.160</td>
      <td>3166</td>
      <td>0.128</td>
      <td>0.126</td>
      <td>0.031</td>
      <td>0.050</td>
      <td>0.067</td>
      <td>2019-09-27 06:36</td>
      <td>2019-09-27 10:44</td>
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

Hence, a naive synchronized pipeline will take 50s to finish 50 requests.

### Result

<p align="center">
<a href="https://gnes.ai">
<img src=".github/data-rate-2.svg" alt="workflow 1 in test" width=60%>
</a>
</p>



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
      <td><a href="https://github.com/gnes-ai/gnes/commit/49150fb"><code>49150fb</code></a></td>
      <td>24.423</td>
      <td>34</td>
      <td>0.094</td>
      <td>0.966</td>
      <td>0.043</td>
      <td>23.185</td>
      <td>0.183</td>
      <td>2019-10-10 04:51</td>
      <td>2019-10-10 05:21</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/17f9287"><code>17f9287</code></a></td>
      <td>24.236</td>
      <td>43</td>
      <td>0.092</td>
      <td>1.034</td>
      <td>0.037</td>
      <td>23.152</td>
      <td>0.035</td>
      <td>2019-10-10 00:33</td>
      <td>2019-10-10 01:03</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/3aab341"><code>3aab341</code></a></td>
      <td>24.280</td>
      <td>43</td>
      <td>0.092</td>
      <td>1.035</td>
      <td>0.038</td>
      <td>23.198</td>
      <td>0.036</td>
      <td>2019-10-09 10:15</td>
      <td>2019-10-09 10:43</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/fc546f0"><code>fc546f0</code></a></td>
      <td>24.227</td>
      <td>43</td>
      <td>0.092</td>
      <td>1.035</td>
      <td>0.038</td>
      <td>23.132</td>
      <td>0.036</td>
      <td>2019-09-30 09:41</td>
      <td>2019-09-30 10:11</td>
      <td><code>v0.0.43-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/83f96d9"><code>83f96d9</code></a></td>
      <td>24.250</td>
      <td>43</td>
      <td>0.093</td>
      <td>1.034</td>
      <td>0.038</td>
      <td>23.166</td>
      <td>0.037</td>
      <td>2019-09-29 12:34</td>
      <td>2019-09-29 13:05</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/4dcf6d0"><code>4dcf6d0</code></a></td>
      <td>24.220</td>
      <td>43</td>
      <td>0.092</td>
      <td>1.035</td>
      <td>0.037</td>
      <td>23.138</td>
      <td>0.034</td>
      <td>2019-09-29 11:57</td>
      <td>2019-09-29 12:27</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/0bb0082"><code>0bb0082</code></a></td>
      <td>24.203</td>
      <td>43</td>
      <td>0.092</td>
      <td>1.033</td>
      <td>0.038</td>
      <td>23.111</td>
      <td>0.037</td>
      <td>2019-09-29 11:23</td>
      <td>2019-09-29 11:50</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/cb4e46a"><code>cb4e46a</code></a></td>
      <td>24.255</td>
      <td>43</td>
      <td>0.092</td>
      <td>1.034</td>
      <td>0.037</td>
      <td>23.170</td>
      <td>0.037</td>
      <td>2019-09-29 04:07</td>
      <td>2019-09-29 04:37</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/a087626"><code>a087626</code></a></td>
      <td>5.928</td>
      <td>86</td>
      <td>0.184</td>
      <td>1.265</td>
      <td>0.099</td>
      <td>2.134</td>
      <td>0.341</td>
      <td>2019-09-27 11:05</td>
      <td>2019-09-27 11:39</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/51837cf"><code>51837cf</code></a></td>
      <td>24.304</td>
      <td>43</td>
      <td>0.091</td>
      <td>1.035</td>
      <td>0.037</td>
      <td>23.220</td>
      <td>0.036</td>
      <td>2019-09-27 06:36</td>
      <td>2019-09-27 10:32</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/51837cf"><code>51837cf</code></a></td>
      <td>24.246</td>
      <td>43</td>
      <td>0.092</td>
      <td>1.035</td>
      <td>0.037</td>
      <td>23.164</td>
      <td>0.035</td>
      <td>2019-09-27 06:36</td>
      <td>2019-09-27 10:47</td>
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

<p align="center">
<a href="https://gnes.ai">
<img src=".github/data-rate-3.svg" alt="workflow 1 in test" width=60%>
</a>
</p>



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
      <td><a href="https://github.com/gnes-ai/gnes/commit/49150fb"><code>49150fb</code></a></td>
      <td>3.398</td>
      <td>221</td>
      <td>0.127</td>
      <td>0.010</td>
      <td>0.058</td>
      <td>0.047</td>
      <td>3.281</td>
      <td>2019-10-10 04:51</td>
      <td>2019-10-10 05:22</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/17f9287"><code>17f9287</code></a></td>
      <td>0.157</td>
      <td>3232</td>
      <td>0.126</td>
      <td>0.124</td>
      <td>0.031</td>
      <td>0.047</td>
      <td>0.063</td>
      <td>2019-10-10 00:33</td>
      <td>2019-10-10 01:05</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/3aab341"><code>3aab341</code></a></td>
      <td>0.158</td>
      <td>3213</td>
      <td>0.127</td>
      <td>0.125</td>
      <td>0.031</td>
      <td>0.052</td>
      <td>0.063</td>
      <td>2019-10-09 10:15</td>
      <td>2019-10-09 10:44</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/fc546f0"><code>fc546f0</code></a></td>
      <td>0.159</td>
      <td>3195</td>
      <td>0.127</td>
      <td>0.123</td>
      <td>0.031</td>
      <td>0.052</td>
      <td>0.064</td>
      <td>2019-09-30 09:41</td>
      <td>2019-09-30 10:12</td>
      <td><code>v0.0.43-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/83f96d9"><code>83f96d9</code></a></td>
      <td>0.160</td>
      <td>3172</td>
      <td>0.128</td>
      <td>0.127</td>
      <td>0.032</td>
      <td>0.053</td>
      <td>0.063</td>
      <td>2019-09-29 12:34</td>
      <td>2019-09-29 13:06</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/4dcf6d0"><code>4dcf6d0</code></a></td>
      <td>0.156</td>
      <td>3245</td>
      <td>0.126</td>
      <td>0.124</td>
      <td>0.031</td>
      <td>0.053</td>
      <td>0.062</td>
      <td>2019-09-29 11:57</td>
      <td>2019-09-29 12:29</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/0bb0082"><code>0bb0082</code></a></td>
      <td>0.155</td>
      <td>3261</td>
      <td>0.125</td>
      <td>0.124</td>
      <td>0.030</td>
      <td>0.050</td>
      <td>0.064</td>
      <td>2019-09-29 11:23</td>
      <td>2019-09-29 11:51</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/cb4e46a"><code>cb4e46a</code></a></td>
      <td>0.156</td>
      <td>3255</td>
      <td>0.125</td>
      <td>0.124</td>
      <td>0.031</td>
      <td>0.052</td>
      <td>0.063</td>
      <td>2019-09-29 04:07</td>
      <td>2019-09-29 04:38</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/a087626"><code>a087626</code></a></td>
      <td>1.623</td>
      <td>601</td>
      <td>0.688</td>
      <td>0.703</td>
      <td>0.351</td>
      <td>0.300</td>
      <td>0.953</td>
      <td>2019-09-27 11:05</td>
      <td>2019-09-27 11:43</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/51837cf"><code>51837cf</code></a></td>
      <td>0.157</td>
      <td>3221</td>
      <td>0.126</td>
      <td>0.125</td>
      <td>0.032</td>
      <td>0.053</td>
      <td>0.062</td>
      <td>2019-09-27 06:36</td>
      <td>2019-09-27 10:34</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/51837cf"><code>51837cf</code></a></td>
      <td>0.159</td>
      <td>3181</td>
      <td>0.128</td>
      <td>0.126</td>
      <td>0.032</td>
      <td>0.055</td>
      <td>0.063</td>
      <td>2019-09-27 06:36</td>
      <td>2019-09-27 10:48</td>
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

As `Router1` and `Router2` are parallel, a naive synchronized implementation will take 25s to finish 50 requests.

### Result

<p align="center">
<a href="https://gnes.ai">
<img src=".github/data-rate-4.svg" alt="workflow 1 in test" width=60%>
</a>
</p>



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
      <td><a href="https://github.com/gnes-ai/gnes/commit/49150fb"><code>49150fb</code></a></td>
      <td>11.946</td>
      <td>60</td>
      <td>0.075</td>
      <td>0.457</td>
      <td>10.694</td>
      <td>0.030</td>
      <td>0.206</td>
      <td>2019-10-10 04:51</td>
      <td>2019-10-10 05:24</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/17f9287"><code>17f9287</code></a></td>
      <td>11.845</td>
      <td>75</td>
      <td>0.075</td>
      <td>0.509</td>
      <td>10.767</td>
      <td>0.030</td>
      <td>0.032</td>
      <td>2019-10-10 00:33</td>
      <td>2019-10-10 01:07</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/3aab341"><code>3aab341</code></a></td>
      <td>11.841</td>
      <td>75</td>
      <td>0.075</td>
      <td>0.507</td>
      <td>10.755</td>
      <td>0.031</td>
      <td>0.030</td>
      <td>2019-10-09 10:15</td>
      <td>2019-10-09 10:46</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/fc546f0"><code>fc546f0</code></a></td>
      <td>11.820</td>
      <td>75</td>
      <td>0.074</td>
      <td>0.508</td>
      <td>10.741</td>
      <td>0.032</td>
      <td>0.036</td>
      <td>2019-09-30 09:41</td>
      <td>2019-09-30 10:14</td>
      <td><code>v0.0.43-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/83f96d9"><code>83f96d9</code></a></td>
      <td>11.824</td>
      <td>75</td>
      <td>0.075</td>
      <td>0.508</td>
      <td>10.750</td>
      <td>0.030</td>
      <td>0.032</td>
      <td>2019-09-29 12:34</td>
      <td>2019-09-29 13:08</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/4dcf6d0"><code>4dcf6d0</code></a></td>
      <td>11.837</td>
      <td>75</td>
      <td>0.075</td>
      <td>0.508</td>
      <td>10.761</td>
      <td>0.032</td>
      <td>0.034</td>
      <td>2019-09-29 11:57</td>
      <td>2019-09-29 12:31</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/0bb0082"><code>0bb0082</code></a></td>
      <td>11.834</td>
      <td>75</td>
      <td>0.074</td>
      <td>0.508</td>
      <td>10.757</td>
      <td>0.030</td>
      <td>0.035</td>
      <td>2019-09-29 11:23</td>
      <td>2019-09-29 11:54</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/cb4e46a"><code>cb4e46a</code></a></td>
      <td>11.820</td>
      <td>75</td>
      <td>0.073</td>
      <td>0.507</td>
      <td>10.742</td>
      <td>0.031</td>
      <td>0.038</td>
      <td>2019-09-29 04:07</td>
      <td>2019-09-29 04:41</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/a087626"><code>a087626</code></a></td>
      <td>5.022</td>
      <td>103</td>
      <td>0.081</td>
      <td>0.633</td>
      <td>0.837</td>
      <td>0.344</td>
      <td>0.289</td>
      <td>2019-09-27 11:05</td>
      <td>2019-09-27 11:48</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/51837cf"><code>51837cf</code></a></td>
      <td>11.834</td>
      <td>76</td>
      <td>0.074</td>
      <td>0.508</td>
      <td>10.759</td>
      <td>0.030</td>
      <td>0.033</td>
      <td>2019-09-27 06:36</td>
      <td>2019-09-27 10:36</td>
      <td><code>latest-alpine</code></td>
    </tr>
    <tr>
      <td><a href="https://github.com/gnes-ai/gnes/commit/51837cf"><code>51837cf</code></a></td>
      <td>11.856</td>
      <td>75</td>
      <td>0.075</td>
      <td>0.509</td>
      <td>10.783</td>
      <td>0.031</td>
      <td>0.033</td>
      <td>2019-09-27 06:36</td>
      <td>2019-09-27 10:51</td>
      <td><code>latest-alpine</code></td>
    </tr>
  </tbody>
</table>