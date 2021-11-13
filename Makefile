all: bdist_wheel

bdist_wheel:
	python setup.py bdist_wheel --universal

sdist:
	python setup.py sdist

build_deb:
	dpkg-buildpackage -us -uc

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf ssh_proxy_tracer/__pycache__/

clean_deb:
	debian/rules clean

.PHONY: all bdist_wheel sdist build_deb clean
