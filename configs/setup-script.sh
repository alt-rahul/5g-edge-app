#downloading prometheus

curl -L https://github.com/prometheus/prometheus/releases/download/v3.4.1/prometheus-3.4.1.linux-amd64.tar.gz > prometheus-3.4.1.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
rm prometheus-*.tar.gz

#downloading grafana

sudo apt-get install -y adduser libfontconfig1 musl
wget https://dl.grafana.com/enterprise/release/grafana-enterprise_12.0.2_amd64.deb
sudo dpkg -i grafana-enterprise_12.0.2_amd64.deb

#downloading nvidia_gpu_exporter

curl -L https://github.com/utkuozdemir/nvidia_gpu_exporter/releases/download/v1.3.2/nvidia-gpu-exporter_1.3.2_linux_amd64.deb > nvidia-gpu-exporter_1.3.2_linux_amd64.deb
sudo dpkg -i nvidia-gpu-exporter_1.3.2_linux_amd64.deb
sudo useradd --system --no-create-home --shell /usr/sbin/nologin nvidia_gpu_exporter
cd /usr/bin
cp nvidia_gpu_exporter /etc/systemd/system
cd 
sudo systemctl daemon-reload
sudo systemctl enable --now nvidia_gpu_exporter


#downloading node exporter

curl -L https://github.com/prometheus/node_exporter/releases/download/v1.9.1/node_exporter-1.9.1.linux-amd64.tar.gz > node_exporter-1.9.1.linux-amd64.tar.gz
tar xvfz node_exporter-*.*-amd64.tar.gz
rm node_exporter-*.*-amd64.tar.gz

#dowloading ollama 
curl -fsSL https://ollama.com/install.sh | sh
OLLAMA_HOST=0.0.0.0 ollama serve