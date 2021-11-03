from setuptools import setup, find_packages


LONG_DESCRIPTION = open("README.md").read()  # pylint:disable=unspecified-encoding,consider-using-with

setup(name="pywsitest",
      version="0.3.8",
      description="PYthon WebSocket Integration TESTing framework",
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      url="https://github.com/gridsmartercities/pywsitest",
      author="Grid Smarter Cities",
      author_email="open-source@gridsmartercities.com",
      license="MIT",
      classifiers=[
          "Intended Audience :: Developers",
          "Development Status :: 3 - Alpha",
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Natural Language :: English"
      ],
      keywords="websocket integration test testing",
      packages=find_packages(exclude=("tests",)),
      install_requires=[
          "websockets",
          "requests"
      ],
      zip_safe=False,
      python_requires=">=3.7")
