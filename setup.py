from distutils.core import setup

setup(
    name='mongo_manager',
    packages=['mongo_manager'],
    version='0.1',
    license='MIT',
    description='Libreria para manejar objetos almacenados en MongoDB, usando la referencia de los CRUDRepository de SpringBoot',
    author='Juan Palma Borda',
    author_email='juanpalmaborda@hotmail.com',
    url='https://github.com/muerterauda/mongo_manager',
    download_url='https://github.com/muerterauda/mongo_manager/archive/v_0_1.tar.gz',
    keywords=['mongo', 'mongodb', 'object', 'reposiroty', 'entity'],
    install_requires=[
        'bson',
        'pymongo',
    ],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
