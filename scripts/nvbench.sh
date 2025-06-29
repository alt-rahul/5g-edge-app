
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

# 3. Now install nvcc 
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

#4. Now inistall nvbench
    git clone https://github.com/NVIDIA/nvbench_demo.git
    cd nvbench_demo
    cmake -DCMAKE_CUDA_ARCHITECTURES=native .
    make
    ./example_bench
