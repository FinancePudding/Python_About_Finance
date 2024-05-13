# Qwen LLM win系统配置指南

## 1.安装环境测试  
我测试了使用 VMware 构建虚拟机的方法进行模型配置，发现并不能够检测和使用本地电脑的GPU环境，只能检测到虚拟出来的CPU计算环境。经过后面测试，发现可以使用win系统的wsl-Ubuntu实现本地配置。同时运行速度和延迟都优于VMware，不需要装配双系统就可以实现。本次配置选择了WSL(Window Subsystem For Linux)中的**Ubuntu 22.04.3 LTS**作为配置安装的系统对象。  

## 2.Qwen LLM配置要求

> python 3.8及以上版本

这里直接选择安装Anaconda环境，方便使用conda命令创建虚拟环境。  
> pytorch 1.12及以上版本，推荐2.0及以上版本     

Pytorch需要提前装配好，不然安装的过程中会发生报错。 
> 建议使用CUDA 11.4及以上（GPU用户、flash-attention用户等需考虑此选项）

CUDA是调用GPU必须配置的程序，如果想要使用GPU加速，必须要下载相应版本的CUDA。flash-attention 是一个在GPU环境下，通过降低数据精度，用来提升推理和计算速度的加速包，对于模型的运行有很大程度的加速效果，这里强烈推荐安装配置。

## 3.Ubuntu的磁盘迁移
我们通过微软appstore下载Ubuntu 22.04.3 LTS的时候，默认安装在本地的C盘下，由于后续下载的大模型和推理所需要的空间相对较大，会出现系统盘崩溃的情况。为了防止出现磁盘空间不足，我们需要将Ubuntu 22.04.3 移动到D盘等，非系统盘之下。详细代码参考了[CSDN论坛](https://blog.csdn.net/weixin_58045467/article/details/124301843)，下面是适合Ubuntu 22.04.3版本的代码，可以直接拷贝运行。

### 3.1 查看WSL的安装和运行情况
``` PowerShell
wsl -v -l
```
```[out]
PS C:\Windows\system32> wsl -l -v
  NAME            STATE           VERSION
* Ubuntu-22.04    Stopped         2
```
### 3.2 关闭正在运行的WSL
``` PowerShell
# 如果WSL正在运行，可以通过如下代码关闭。运行的过程中进行后续操作会发生一系列问题，所以一定要确保WSL处于关闭状态。
wsl --shutdown
```
### 3.3 将Ubuntu-22.04 压缩并导出到相应目录，这里的目录需要提前在Win系统中创建。
```PowerShell
 wsl --export Ubuntu-22.04 D:\UbuntuWSL\ubuntu.tar
```
### 3.4 将原来的Ubuntu-22.04 账户进行注销，释放C盘空间。
```PowerShell
wsl --unregister Ubuntu-22.04
```
### 3.5 导入Ubuntu，名称与原来注销的Ubuntu名称一致
这里推荐导入名称和注销的账户名称一致，这样还可以使用原来的终端进入到新导入的Ubuntu中。
```PowerShell
wsl --import Ubuntu-22.04 D:\UbuntuWSL\ D:\UbuntuWSL\ubuntu.tar --version 2
```
### 3.6 导入Ubuntu名称与原来不一致时，可以使用PowerShell连接
```PowerShell
# 这里将导入的Ubuntu命名为MyUbuntu，则win系统中的Ubuntu 22.04.3 LTS终端就无法连接到新导入的MyUbuntu中
wsl --import MyUbuntu D:\UbuntuWSL\ D:\UbuntuWSL\ubuntu.tar --version 2
# 通过PowerShell连接MyUbuntu，输入命令运行后PowerShell终端就连接到了MyUbuntu中。
wsl -d MyUbuntu
```
## 4.[Anaconda](https://docs.anaconda.com/free/anaconda/install/linux/)在Ubuntu 22.04.3 中的安装
以下命令在Ubuntu 22.04.3 终端中输入运行，这里推荐直接使用root用户进行登录，权限较多，更加方便一些。
### 4.1 更新并升级apt包管理工具
```Ubuntu
# 切换到home目录，方便进行管理
cd /home/
# 在家目录创建文件夹
mkdir andy
# 切换到新建目录之下，后续下载的内容除了默认安装位置的都在此目录下。
cd andy
# apt包管理更新
sudo apt update
sudo apt upgrade
```

### 4.2 安装Debain的依赖包(Ubuntu 属于Debain的产品)
```Ubuntu
apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 -y
```
### 4.3 查看本地Ubuntu 22.04.3的操作系统型号
```Ubuntu
arch
```
### 4.4 下载想要的Anaconda版本，这里选择的是2024.02-1版本
```Ubuntu
curl -O https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
```
### 4.5 安装Anaconda版本
```Ubuntu
# 这里的路径需要指定所在的下载目录
bash ~/Downloads/Anaconda3-2024.02-1-Linux-x86_64.sh
```
### 4.6 测试是否安装成功
```Ubuntu
source <PATH_TO_CONDA>/bin/activate
conda init
```
### 4.4 选择安装想要的Anaconda版本，这里选择的是2024.02-1版本
```Ubuntu
curl -O https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
```
### 4.4 选择安装想要的Anaconda版本，这里选择的是2024.02-1版本
```Ubuntu
curl -O https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
```
## 5.安装[CUDA](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network)
### 5.1 下载CUDA 12.4
```Ubuntu
# 文件较大，下载过程会相对较慢一些
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-4
```
### 5.1 下载CUDA 12.4
```Ubuntu
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-4
```

### 5.2 设置CUDA的环境变量
```Ubuntu
# 打开/root/.bashrc的配置文件
vim ~/.bashrc
```
通过vim编译器打开之后，跳转到文件的最后一行，按下键盘的<o>键，可以在下一行,直接插入如下代码 
```vim
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-12.4/lib64  
export PATH=/usr/local/cuda-12.4/bin${PATH:+:${PATH}}  
export CUDA_HOME=$CUDA_HOME:'/usr/local/cuda-12.4'  
```
复制粘贴文本后，先按下<Esc>键，后在终端中输入如下命令，保存修改并退出文件，代码运行之后就退出了vim编辑器的界面，进入Ubuntu的终端命令行。
```vim
:wq
```

### 5.3 重启终端
```Ubuntu
reboot
```

### 5.4 检验配置安装是否成功
```Ubuntu
# 检验Ubuntu是否能够检测到本地的英伟达显卡
nvidia-smi
# 检验CUDA是否安装成功
nvcc -V
```
## 6.安装[pytroch](https://pytorch.org/get-started/locally/)
```Ubuntu
pip3 install torch torchvision torchaudio
```
## 7.配置Qwen_1.8B_Chat相关安装包
### 7.1 创建虚拟环境
```Ubuntu
conda create -n QwenLLM python=3.12 -c conda-forge
```
### 7.2 激活虚拟环境
```Ubuntu
conda activate QwenLLM
```
### 7.3 安装[Qwen_1.8B_Chat](https://modelscope.cn/models/qwen/Qwen-1_8B-Chat/summary)的依赖性
```Ubuntu
pip install transformers==4.32.0 accelerate tiktoken einops scipy transformers_stream_generator==0.0.4 peft deepspeed
```
### 7.4 下载安装flash-attention加速包
```Ubuntu
git clone https://github.com/Dao-AILab/flash-attention
cd flash-attention && pip install .
# 下方安装可选，安装可能比较缓慢。
# 这个安装选项目前已经更新合并，在包中的指定文件中得到了相同效果的实现，后续模型运行的过程中发生的提示可以选择忽视。
# pip install csrc/layer_norm 
# 这个选项可以进行正常安装
pip install csrc/rotary
```
### 7.5 下载模型到本地，并进行相应的测试调节。
```Ubuntu
conda activate QwenLLM
```
