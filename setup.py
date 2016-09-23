
from distutils.core import setup
setup(
        name='proxyrentalapi',
        version='0.0.1',
        author="Chaps",
        author_email="drumchaps@gmail.com",
        maintainer="Chaps",
        maintainer_email="drumchaps@gmail.com",
        url="https://bitbucket.org/drumchaps/proxyrentalapi",
        py_modules=[
            #BUILT IN MODULES
            #'client',
            #'global_info'
        ],   
        packages  = [
            #'urlparse',
            "proxyrentalapi",
            #'md5',
            #'xml',
            #'traceback',
        ],
        package_dir={'proxyrentalapi': 'src/proxyrentalapi'},
        install_requires = [
            "requests",
        ]
)
