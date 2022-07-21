from setuptools import setup, find_packages

setup(
    name="esnt-intern-mini-spider-ymh",
    version="0.1.0",
    author="易旻晗",
    author_email="minhan.yi@70capital.com",
    description="a mini spider.",
    license="MIT",
    url="",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'chardet>=5.0.0',
        'lxml>=4.9.1',
        'requests>=2.28.1'
    ],
    zip_safe=True,
)
