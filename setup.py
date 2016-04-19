from distutils.core import setup

setup(
    name='le_provisioning',
    packages=['le_provisioning'],
    version='0.5',
    description='A small set of scripts to install SSL certs on WHM using LetsEncrypt',
    author='Nick Bagley',
    author_email='nick@thrivehive.com',
    url='https://github.com/teasea33/le-provisioning.git',
    download_url='https://github.com/teasea33/le-provisioning/archive/0.1.zip',
    keywords=['letsencrypt', 'ssl', 'whm', 'cpanel'],
    license='GPLv3',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 2 - Pre-Alpha"
    ]
)
