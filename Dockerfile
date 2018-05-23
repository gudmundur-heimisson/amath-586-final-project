FROM debian
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
  build-essential pkg-config \
  cmake gfortran git \
  python3 python3-dev python3-pip
# Install OpenBLAS
WORKDIR /
RUN git clone https://github.com/xianyi/OpenBLAS --depth=1 --branch=v0.2.20 --recursive
RUN mkdir /OpenBLAS/build
WORKDIR /OpenBLAS/build
RUN cmake .. && \
  make -j8 install
# Install NumPy
RUN python3 -m pip install cython
WORKDIR /
RUN git clone https://github.com/numpy/numpy --depth=1 --branch=v1.14.3 --recursive
WORKDIR /numpy
ADD numpy.site.cfg site.cfg
RUN python3 setup.py build_ext --inplace -j8 && python3 setup.py install
WORKDIR /root
RUN python3 -c 'import numpy; print(numpy.__config__.show())'
# Install Boost
WORKDIR /
RUN git clone https://github.com/boostorg/boost --depth=1 --branch=boost-1.67.0 --recursive
WORKDIR /boost
RUN ./bootstrap.sh --with-libraries=python --with-python=python3 && \
    ./b2 && \
    ./b2 install
# Build the module
WORKDIR /app
ADD . /app
RUN cmake . && make -j8
RUN python3 test.py
