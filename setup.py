from setuptools import setup

setup(name='flight_logs', version='2023.12.1',
      description='Tools for working with flight history',
      url='https://github.com/GrayTaylor/flight_logs',
      author='Graeme Taylor',
      license='MIT License',
      packages=['flight_logs'],
      install_requires=['geopy>=2.4.1',
                        'plotly>=5.9.0',
                        'pandas>=2.0.3'],
      python_requires=">=3.11")
