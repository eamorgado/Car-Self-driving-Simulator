# Getting Started - CARLA
[Docs][docs-url] -> [Getting Started][getting-started-url] -> CARLA

## Get CARLA version 0.9.10.1

During this project we used [CARLA V0.9.10.1][carla-0.9.10.1]. You can checkout the releases [here][carla-releases]. This file is approximately 4GB

```bash
wget https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.10.1.tar.gz
```

We were forced to move to windows version sice we were expiriencing some issues with CARLA and NVIDIA drivers in Linux 

## Configure CARLA for server use
If you only want to use CARLA as a server and connect to it using the clients you can do so with their docker image.

First you need to set up the NVIDIA driver in docker

### NVIDIA Driver for Docker
Set up the stable repository and GPG key
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```

Install the `nvidia-docker2` package and dependencies after updating the package list
```bash
sudo apt-get update

sudo apt-get install -y nvidia-docker2
```

Now, restart the docker daemon
```bash
sudo systemctl restart docker
```

Test the setup
```bash
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

This should give you a similar output
```bash
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 450.51.06    Driver Version: 450.51.06    CUDA Version: 11.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            On   | 00000000:00:1E.0 Off |                    0 |
| N/A   34C    P8     9W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```



## Installing requirements

To run any script we will need to hae installed **Python3.7**, and will need to install `pygame` and `numpy`. The python version must be a **64 bit version**.

Note, if you have multiple versions you can run the scripts with `py -3.7 script.py` this way you will be able to import the carla module


## Using CARLA

Since we have to mode to Windows we have no way of testing the Linux version, on Windows all you need to do is to run the `CarlaUE4.exe` executable file, this wil launch the carla graphical server, this will be **GPU bound**, they recommend the use of at least 4GB of VRAM.



[docs-url]: https://github.com/eamorgado/Car-Self-driving-Simulator/blob/main/README.md
[getting-started-url]: https://github.com/eamorgado/Car-Self-driving-Simulator/blob/main/Docs/GettingStarted/GettingStarted.md
[carla-0.9.10.1]: https://github.com/carla-simulator/carla/releases/tag/0.9.10.1
[carla-releases]: https://github.com/carla-simulator/carla/releases
