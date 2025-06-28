git clone https://github.com/NVIDIA/nvbench_demo.git

cd nvbench_demo

cmake -DCMAKE_CUDA_ARCHITECTURES=native .

sudo apt update
sudo apt install libssl-dev
sudo apt install cmake


#had an error with cmake (now I need to install)

wget https://github.com/Kitware/CMake/releases/download/v4.1.0-rc1/cmake-4.1.0-rc1.tar.gz
tar -xf cmake-4.1.0-rc1.tar.gz
cd cmake-4.1.0-rc1
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local
make -j$(nproc)
sudo make install

#this may not work, but there is a fix to this:
sudo rm -rf /usr/local/bin/cmake /usr/local/bin/ctest /usr/local/bin/cpack /usr/local/bin/cmake-gui
sudo rm -rf /usr/local/share/cmake-*
sudo rm -rf /usr/local/lib/cmake

#redo lines 9-23 above, check version if it doesn't work do the following:
echo $PATH
export PATH=/usr/local/bin:$PATH
source ~/.bashrc

#to install cuda toolkit
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.9.1/local_installers/cuda-repo-ubuntu2204-12-9-local_12.9.1-575.57.08-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-9-local_12.9.1-575.57.08-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-9-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-9
