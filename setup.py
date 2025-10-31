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
    entry_points={
        'console_scripts': [
            'update_hints = vocab_learner.tools.update_hints:main',
            'display_q_table = vocab_learner.tools.display_q_table:main',
            'vocab_learner_api = vocab_learner.examples.app:main', 
        ],
    },
    description='A modular Q-learning based vocabulary hint system',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Manohar Sai Jasti',
    author_email='manoharsai.jasti@icloud.com',
    url='https://github.com/manoharsai9/vocab-learner',
    license='MIT',
    keywords='vocabulary learning q-learning edtech',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)