# [Choice] Python version (use -bookworm or -bullseye variants on local arm64/Apple Silicon): 3, 3.13, 3.12, 3.11, 3.10, 3.9, 3-bookworm, 3.13-bookworm, 3.12-bookworm, 3.11-bookworm, 3.10-bookworm, 3.9-bookworm, 3-bullseye, 3.13-bullseye, 3.12-bullseye, 3.11-bullseye, 3.10-bullseye, 3.9-bullseye, 3-buster, 3.12-buster, 3.11-buster, 3.10-buster, 3.9-buster
ARG VARIANT=3-bookworm
FROM python:${VARIANT}

# >>> SPEEDUP zh-CN
RUN test -f /etc/apt/sources.list && \
    sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list || \
    sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list || \
    exit 0

# Compatible with DEB822
RUN test -f /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources || \
    sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources || \
    exit 0

# Setup pypi mirrors
RUN pip config set --global global.index-url "https://mirrors.aliyun.com/pypi/simple" || \
    exit 0 
# && pip config set global.extra-index-url "<url1> <url2>..." # extra index like pytorch 

# <<< SPEEDUP zh-CN

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    # Remove imagemagick due to https://security-tracker.debian.org/tracker/CVE-2019-10131
    && apt-get purge -y imagemagick imagemagick-6-common 

# Temporary: Upgrade python packages due to https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40897 and https://github.com/advisories/GHSA-2mqj-m65w-jghx
# They are installed by the base image (python) which does not have the patch.
RUN python3 -m pip install --upgrade \
    setuptools==75.6.0 \
    gitpython==3.1.41

RUN echo 'options("repos" = c(CRAN="https://mirrors.tuna.tsinghua.edu.cn/CRAN/"))' >> ~/.Rprofile

# Manage the lifecycle of dify plugins.
RUN wget https://github.com/langgenius/dify-plugin-daemon/releases/download/0.0.6/dify-plugin-linux-amd64 && \
    chmod +x dify-plugin-linux-amd64 && mv ./dify-plugin-linux-amd64 /usr/local/bin/dify