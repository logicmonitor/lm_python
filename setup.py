from setuptools import setup

setup(name='lm_python',
      version='1.0',
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
      packages=['lm_python'],
      install_requires=[
          'datetime',
          'logging'
      ],
      scripts=[
          'bin/collector_add.py',
          'bin/collector_remove.py',
          'bin/collector_sdt.py',
          'bin/host_add.py',
          'bin/host_info.py',
          'bin/host_remove.py',
          'bin/host_sdt.py',
          'bin/host_update.py',
          'bin/hostgroup_add.py',
          'bin/hostgroup_info.py',
          'bin/hostgroup_remove.py',
          'bin/hostgroup_sdt.py',
          'bin/hostgroup_update.py'
      ],
      zip_safe=False)
