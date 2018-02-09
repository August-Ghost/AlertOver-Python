from setuptools import setup

setup(
    name='alertover',
    version='1.0.0',
    packages=['alertover'],
    url='https://github.com/August-Ghost/alertover-python',
    license='MIT',
    author='Ghost',
    author_email='',
    description='Push message form your code to your devices with AlertOver. See: https://www.alertover.com/',
    keywords=["AlertOver", "pushing", "message"],
    install_requires=[
        'aiohttp >= 2.0.0',
        'requests >= 1.0.0'
      ],
)
