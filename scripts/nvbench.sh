
# 1. first install cmake and it dependencies
    sudo apt update
    sudo apt install libssl-dev
    sudo apt install cmake

# 2. install most updated version of cmake
    wget https://github.com/Kitware/CMake/releases/download/v4.1.0-rc1/cmake-4.1.0-rc1.tar.gz
    tar -xf cmake-4.1.0-rc1.tar.gz
    cd cmake-4.1.0-rc1
    mkdir build && cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local
    make -j$(nproc)
    sudo make install
    #check if cmake version is the right version
    cmake --version # if it is showing an older version, continue to do the following
    #change path location
    echo $PATH
    export PATH=/usr/local/bin:$PATH
    source ~/.bashrc
    #check again - should work (worked for me atleast)
    cmake --version

# 3. now install nvcc 
    apt install nvidia-cuda-toolkit
    #check version
    nvcc --version
    #to install updated cuda toolkit (make sure to download the right installer, go this website: https://developer.nvidia.com/cuda-downloads)
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
    sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
    wget https://developer.download.nvidia.com/compute/cuda/12.9.1/local_installers/cuda-repo-ubuntu2004-12-9-local_12.9.1-575.57.08-1_amd64.deb
    sudo dpkg -i cuda-repo-ubuntu2004-12-9-local_12.9.1-575.57.08-1_amd64.deb
    sudo cp /var/cuda-repo-ubuntu2004-12-9-local/cuda-*-keyring.gpg /usr/share/keyrings/
    sudo apt-get update
    sudo apt-get -y install cuda-toolkit-12-9
    #check nvcc version
    nvcc --version
    #change path location
    export PATH=/usr/local/cuda-12.9/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/cuda-12.9/lib64:$LD_LIBRARY_PATH
    #set pointers to new cuda version
    sudo update-alternatives --install /usr/local/cuda cuda /usr/local/cuda-12.9 1
    sudo update-alternatives --set cuda /usr/local/cuda-12.9
    sudo update-alternatives --display cuda
    #check pointers
    ls -l /usr/local/cuda

# 4. now inistall nvbench
    git clone https://github.com/NVIDIA/nvbench_demo.git
    cd nvbench_demo
    cmake -DCMAKE_CUDA_ARCHITECTURES=native .
    make
    ./example_bench

# 5. now the result look similar to this:

# Benchmark Results

## sleep_benchmark

### [0] Tesla V100-PCIE-16GB

# | Duration (us) | Samples |  CPU Time  | Noise  |  GPU Time  | Noise  | Samples | Batch GPU  |
# |---------------|---------|------------|--------|------------|--------|---------|------------|
# |             0 |  19987x |  15.729 us |  3.50% |   3.789 us | 12.28% | 304673x |   1.642 us |
# |             5 |  18732x |  19.723 us |  6.64% |   7.842 us |  6.29% |  81369x |   6.145 us |
# |            10 |  17308x |  24.880 us |  1.85% |  12.980 us |  3.90% |  44389x |  11.264 us |
# |            15 |  16042x |  29.985 us | 15.20% |  18.084 us |  2.77% |  30518x |  16.384 us |
# |            20 |  14948x |  35.168 us | 13.08% |  23.221 us |  2.09% |  23252x |  21.504 us |
# |            25 |  13989x |  40.314 us | 11.88% |  28.345 us |  1.73% |  18780x |  26.624 us |
# |            30 |  13129x |  45.355 us |  1.00% |  33.447 us |  1.47% |  15751x |  31.744 us |
# |            35 |  12333x |  50.574 us |  0.91% |  38.604 us |  1.29% |  13564x |  36.864 us |
# |            40 |  11456x |  55.665 us |  0.90% |  43.698 us |  1.14% |  11953x |  41.984 us |
# |            45 |  10480x |  59.783 us |  0.79% |  47.776 us |  1.05% |  10935x |  46.080 us |
# |            50 |   9456x |  64.983 us |  0.68% |  52.913 us |  0.91% |   9884x |  51.200 us |
# |            55 |   8624x |  70.039 us |  8.34% |  58.034 us |  0.85% |   9017x |  56.320 us |
# |            60 |   7920x |  75.187 us |  0.59% |  63.153 us |  0.76% |   8290x |  61.440 us |
# |            65 |   7328x |  80.365 us |  0.61% |  68.279 us |  0.74% |   7671x |  66.560 us |
# |            70 |   6816x |  85.391 us |  0.59% |  73.374 us |  0.68% |   7138x |  71.680 us |
# |            75 |   6368x |  90.558 us |  0.48% |  78.541 us |  0.61% |   6675x |  76.800 us |
# |            80 |   5984x |  95.625 us |  0.57% |  83.633 us |  0.65% |   6268x |  81.920 us |
# |            85 |   5648x | 100.749 us |  0.46% |  88.753 us |  0.58% |   5907x |  87.040 us |
# |            90 |   5392x | 104.916 us |  0.43% |  92.874 us |  0.52% |   5648x |  91.136 us |
# |            95 |   5104x | 110.169 us |  7.98% |  97.984 us |  0.51% |   5353x |  96.256 us |
# |           100 |   4849x | 115.262 us |  0.41% | 103.128 us |  0.48% |   5088x | 101.376 us |
