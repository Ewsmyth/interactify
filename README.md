# Interactify
 Flask Social Media site hosted with Docker
## Update Ubuntu Server
```
sudo apt update && sudo apt upgrade -y
```

## Install Docker on Ubuntu Server

##### Add Docker's official GPG key:
```
sudo apt-get install ca-certificates curl gnupg
```
```
sudo install -m 0755 -d /etc/apt/keyrings
```
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
```
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
##### Add the repository to Apt sources:
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
```
sudo apt-get update
```
##### Install Docker packages:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```
## Install Portainer with Docker
##### Create a volume that Portainer Server will use to store its database:
```
sudo docker volume create portainer_data
```
##### Download and install Portainer Server:
```
sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```
##### Login to the admin account:
```
https://<serverip>:9443
```
## Download and install Interactify with Docker:

##### You can run this command in any directory you want I just run it from the usr/<username> directory
```
sudo git clone https://github.com/Ewsmyth/interactify.git
```
##### This should be altered to the proper path to the directory you cloned the git into
```
cd interactify
```
##### The period is if you are inside the "interactify" directory if you are not then you should replace this with the path to the interactify directory
```
sudo docker build -t interactify-image .
```
##### Setup the database volume for persistent storage
```
sudo docker volume create interactify-data
```
##### Setup the userposts volume for persistent storage
```
sudo docker volume create interactify-uploads
```
##### Install Interactify with Docker run
```
sudo docker run -d -p 8585:8585 --restart=unless-stopped \
    -v interactify-data:/var/lib/docker/volumes/interactify-data \
    -v interactify-uploads:/var/lib/docker/volumes/interactify-uploads \
    interactify-image
```