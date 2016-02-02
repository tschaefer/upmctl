from setuptools import setup

setup(
    name='confluencectl',
    version='0.0.1',
    packages=['confluencectl'],
    install_requires=['requests >= 2.9.1'],
    entry_points={'console_scripts': ['confluencectl=confluencectl.__main__:main']},
    author='Tobias Schäfer',
    author_email='confluencectl@blackoxorg',
    url='https://github.com/tschaefer/confluencectl',
    description="confluencectl - Control Atlassian Confluence from the console.",
    license='BSD',
    include_package_data=True,
    zip_safe=False
)
