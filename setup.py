from setuptools import find_packages, setup
from ssh_proxy_tracer.main import VERSION


setup(
    name='ssh_proxy_tracer',
    version=str(VERSION),
    packages=find_packages(),
    package_data={'ssh_proxy_tracer': ['bpf_tcp_connect.c']},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    entry_points={
        'console_scripts': ['ssh-proxy-tracer=ssh_proxy_tracer.main:main'],
    }
)
