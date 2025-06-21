#downloading prometheus

curl -L https://github.com/prometheus/prometheus/releases/download/v3.4.1/prometheus-3.4.1.linux-amd64.tar.gz > prometheus-3.4.1.linux-amd64.tar.gz

tar xvfz prometheus-*.tar.gz

# cd prometheus-*

#downloading grafana

sudo apt-get install -y adduser libfontconfig1 musl

wget https://dl.grafana.com/enterprise/release/grafana-enterprise_12.0.2_amd64.deb

sudo dpkg -i grafana-enterprise_12.0.2_amd64.deb

#downloading nvidia_gpu_exporter

VERSION=1.3.1
wget https://github.com/utkuozdemir/nvidia_gpu_exporter/releases/download/v${VERSION}/nvidia_gpu_exporter_${VERSION}_linux_x86_64.tar.gz
tar -xvzf nvidia_gpu_exporter_${VERSION}_linux_x86_64.tar.gz
mv nvidia_gpu_exporter /usr/bin
sudo useradd --system --no-create-home --shell /usr/sbin/nologin nvidia_gpu_exporter

#downloading node exporter

curl -L https://github.com/prometheus/node_exporter/releases/download/v1.9.1/node_exporter-1.9.1.linux-amd64.tar.gz > node_exporter-1.9.1.linux-amd64.tar.gz

tar xvfz node_exporter-*.*-amd64.tar.gz


# editing the prometehus config file

YML_FILE = '/root/prometheus/prometheus.yml'

cat <<EOF > "$YML_FILE"
# my global config
global:
    scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.

  # run prometheus
  - job_name: "prometheus"

    # prometheus port
    static_configs:
      - targets: ["0.0.0.0:9090"]
          app: "prometheus"
  
  # node exporter
  - job_name: node

    # node exporter port
    static_configs:
      - targets: ['localhost:9100']

  # running nvidia-gpu-exporter 
  - job_name: 'nvidia_gpu'
    
    # gpu exporter port
    static_configs:
      - targets: ['localhost:9835']

EOF

#creating prometheus as a service

cd ..


SERVICE_NAME = "prometheus.service"
SERVICE_PATH = "etc/systemd/system/$SERVICE_NAME"

sudo tee "$SERVICE_PATH" > /dev/null <<EOF 
[Unit]
Description=ROT13 demo service
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=centos
ExecStart=/root/prometheus

[Install]
WantedBy=multi-user.target


