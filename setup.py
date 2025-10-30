from setuptools import setup, find_packages

setup(
    name='vocab_learner',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
    ],
    extras_require={
        'api': ['flask'],
    },
    description='A modular Python package for a Q-learning based vocabulary hint system',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Manohar Sai Jasti',
    author_email='manoharsai.jasti@gmail.com',  # Update with your email
    url='https://github.com/manoharsai9/vocab-learner',
    license='MIT',
    keywords='vocabulary learning q-learning edtech',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)