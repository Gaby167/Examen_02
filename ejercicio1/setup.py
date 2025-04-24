from setuptools import find_packages, setup

package_name = 'ejercicio1'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],

    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/launch.py']),
        ('share/' + package_name + '/urdf', ['urdf/brazo_ej1.urdf']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gabriela',
    maintainer_email='gabriela.capurata@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'c_directa = ejercicio1.c_directa:main',
            'c_inversa = ejercicio1.c_inversa:main',
            'dh = ejercicio1.dh:main',
            'jacobiana = ejercicio1.jacobiana:main',
        ],
    },

)
