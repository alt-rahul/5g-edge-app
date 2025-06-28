git clone https://github.com/NVIDIA/nvbench_demo.git

cd nvbench_demo

cmake -DCMAKE_CUDA_ARCHITECTURES=native .

#had an error with cmake (now I need to install)

wget https://github.com/Kitware/CMake/releases/download/v4.1.0-rc1/cmake-4.1.0-rc1.tar.gz
tar -xf cmake-4.1.0-rc1.tar.gz
cd cmake-4.1.0-rc1
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local

#if you get an openSSL error then do the following:
sudo apt update
sudo apt install libssl-dev

#then continue wit the followign
cd build
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