__doc__ = """
uliweb app collections for admin and new style based on bootstrap3 and AdminLTE
"""

from uliweb.utils.setup import setup
import uliweb_peafowl

setup(name='uliweb_peafowl',
    version=uliweb_peafowl.__version__,
    description="Admin app for uliweb",
    long_description=__doc__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    packages = ['uliweb_peafowl'],
    platforms = 'any',
    keywords='uliweb app admin',
    author=uliweb_peafowl.__author__,
    author_email=uliweb_peafowl.__author_email__,
    url=uliweb_peafowl.__url__,
    license=uliweb_peafowl.__license__,
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'uliweb_apps': [
          'helpers = uliweb_peafowl',
        ],
    },
)
