from setuptools import setup

setup(name='logicmonitor_core',
      version='1.0.7.6',
      description='LogicMonitor API python classes',
      long_description='LogicMonitor is a cloud-based, full stack, IT \
          infrastructure monitoring solution that allows you to manage your \
          infrastructure from the cloud. lm_python contains a set of python \
          classes which can be used to manage your LogicMonitor account \
          programmatically.',
      url='https://github.com/logicmonitor/lm_python',
      keywords='LogicMonitor cloud monitoring infrastructure',
      author='LogicMonitor',
      author_email='jeff.wozniak@logicmonitor.com',
      license='MIT',
      packages=['logicmonitor_core'],
      install_requires=[
          'datetime',
          'logging'
      ],
      zip_safe=False)
