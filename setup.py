from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass


setup(
    name='httpie-oauth2',
    description='OAuth2 plugin for HTTPie.',
    long_description=open('README.rst').read().strip(),
    version='0.1.0',
    author='Brian Demers',
    author_email='bdemers@apache.org',
    license='BSD',
    url='https://github.com/bdemers/httpie-oauth2',
    download_url='https://github.com/bdemers/httpie-oauth2',
    py_modules=['httpie_oauth2'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_oauth2 = httpie_oauth2:OAuth2Plugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0',
        'requests-oauthlib>=0.8.0'  
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Environment :: Plugins',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)