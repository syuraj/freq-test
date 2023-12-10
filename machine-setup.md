
# Install Docker
* https://oracle-base.com/articles/linux/docker-install-docker-on-oracle-linux-ol8

```
dnf install -y dnf-utils zip unzip
dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
dnf remove -y runc
dnf install -y docker-ce --nobest
systemctl enable docker.service
systemctl start docker.service
sudo usermod -aG root opc
```
