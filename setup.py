from setuptools import setup, find_packages


setup(
    name='Hearthstone rebuild',
    version='a0.1',
    author=u'Björn Brandt',
    packages=find_packages(),
    scripts=['main.py'],
    install_requires=['pygame'],

    package_data={
        'gui': ['*.png', '*.bmp']
    }
)
