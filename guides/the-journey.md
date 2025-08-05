# Progress Made

> “It's not the destination, it's the journey” - Ralph Waldo Emerson

This document will contain descriptive information about the progress made in the past few weeks. *Warning: Because I'm working on a difficult project,  as a form of entertainment, I made the weekly presenations a complete joke but presented them with all seriousness and with real progress updates. 


### Week 1

- [x] Get started with Edge
  - [x] Understanding what is Edge, why is it useful, and what is it primarily used for
  - [x] Look at existing research papers that explained Edge 
- [x] Finish weekly presentation: [Week 1](../presentations/Week1.pptx)

### Week 2
- [x] Make a future roadmap
  - [x] What exactly are we trying to acheive? - creating Edge benchmarks that'll help the scheduler
  - [x] What are important steps? - look at existing benchmarks, collect data (when running AI applications), integrate our bechmarks with exisiting ones and potentially develop an ML model. 
- [x] Using orbit
  - [x] Learning how to `ssh` into nodes, loading images, and etc.
- [x] Finish weekly presentation: [Week 2](../presentations/Week2.pptx)

### Week 3
- [x] Setting up services
  - [x] Had to set up [Prometehus](https://prometheus.io/), [Grafana](https://grafana.com/), [Nvidia Exporter](https://github.com/utkuozdemir/nvidia_gpu_exporter)
  - [x] Creating an image (`rahulisbetter.ndz`) to load dev enviornment on to any node easier
  - [x] Explored olllama and tried running LLMs on nodes with GPUs (Tesla V100)
- [x] Finish weekly presentation: [Week 3](../presentations/Week3.pptx)

### Week 4
- [x] Creating a pipeline
  - [x] Finalized the script that allows to fetch live metrics Prometheus and store it as a doc in [MongoDB](https://www.mongodb.com/)
  - [x] Found a way to collect LLM performce metric information from ollama locally 
  - [x] Wrap up making a *standardized test* to test LLMs while being used on different nodes
- [X] Create a website, go check it out <a href="https://5g-edge-apps.vercel.app/" target="_blank">here</a>
- [x] Finish weekly presention: [Week 4](../presentations/Week4.pptx)

### Week 5
- [X] Fine grain our roadmap
  - [x] After my advisor had redefined our goal, I was able to break down what I had to do each week
  - [x] Set up a two nodes, one with prometheus and another with `nvidia_gpu_exporter` and `node_exporter`
  - [x] Find the system utilization of both those exporters by pinging `nvidia-smi` and `top` every second for 5 mins with and without them running in the background.
  - [ ] Artifically load the GPU and CPU using *nvbench* and *stress-ng* (respectively) on differnt load percentages 
  - [x] Conduct a initial benchmark using Phoronix Test Suite on `sb2` node on cosmos
- [X] Finish weekly presentation: [Week 5](../presentations/Week5.pptx)

### Week 6
- [x] Init stage stress testing
  - [x] Finish artfically loading and stress testing the GPU using *gpu-burn*
  - [x] Developed a script to collect live GPU metrics while sending Ollama requests
  - [x] Collected enough GPU metrics data to create a baseline benchmark for utilizing the GPU for non-AI related tasks
- [x] Finish weekly presentation: [Week 6](../presentations/Week6.pptx)

### Week 7
- [x] Created a full pipeline where I can asynchronously collect gpu metrics while sending ollama prompt requests
- [x] Successfully conducted a sample test with a pool different prompts 
- [x] Did a basic EDA to understand the metric information and figure out which gpu metrics are more impactful
- [x] Finish weekly presentation: [Week 7](../presentations/Week7.pptx)

### Week 8
- [x] Visualized our metric data as a time series to see the flucations in utilization and other metrics
- [X] Did statistical analysis on the correlation between metric and response time
- [x] Was introduced to the scheduling problem that we're trying to solve
- [x] Finished weekly presentation: [Week 8](../presentations/Week8.pptx)

### Week 9 
- [x] Conducted tests on a few more different GPUs (Tesla V100 16GB, Tesla A100 40GB)
- [x] Feature selection by finding correlation between metrics
- [x] Created an MLP to estimate the weights needed to fine the linear combination of the benchmark (but was unnecessary)
- [x] Transitioned to using Lasso (the L1 regularizer) to fine the relevant coeficients to estimate the response time
- [x] Finished weekly presention: [Week 9](../presentations/Week9.pptx)


### Week 10
- [x] Finalized the benchmarks scoring
- [x] Finished poster 
- [x] Finished final presentation

