from setuptools import find_packages, setup

package_name = 'lemov'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='leoni',
    maintainer_email='leoni@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'move = lemov.moer:main',
            'sensori= lemov.sensores:main',
            'movisen = lemov.movisen:main',
        ],
    },
)
