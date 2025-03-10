#!/usr/bin/env python3
"""Setup for the reference implementation of the CWL standards."""
import os
import sys
import warnings

import setuptools.command.egg_info as egg_info_cmd
from setuptools import setup

if os.name == "nt":
    warnings.warn(
        "The CWL reference runner (cwltool) no longer supports running "
        "CWL workflows natively on MS Windows as its previous MS Windows "
        "support was incomplete and untested. Instead, please see "
        "https://pypi.org/project/cwltool/#ms-windows-users "
        "for instructions on running cwltool via "
        "Windows Subsystem for Linux 2 (WSL2). If don't need to execute "
        "CWL documents, then you can ignore this warning, but please "
        "consider migrating to https://pypi.org/project/cwl-utils/ "
        "for your CWL document processing needs."
    )

SETUP_DIR = os.path.dirname(__file__)
README = os.path.join(SETUP_DIR, "README.rst")

try:
    import gittaggers

    Tagger = gittaggers.EggInfoFromGit
except ImportError:
    Tagger = egg_info_cmd.egg_info

NEEDS_PYTEST = {"pytest", "test", "ptr"}.intersection(sys.argv)
PYTEST_RUNNER = ["pytest-runner", "pytest-cov"] if NEEDS_PYTEST else []
USE_MYPYC = False
# To compile with mypyc, a mypyc checkout must be present on the PYTHONPATH
if len(sys.argv) > 1 and sys.argv[1] == "--use-mypyc":
    sys.argv.pop(1)
    USE_MYPYC = True
if os.getenv("CWLTOOL_USE_MYPYC", None) == "1":
    USE_MYPYC = True

if USE_MYPYC:
    mypyc_targets = [
        "cwltool/argparser.py",
        "cwltool/builder.py",
        "cwltool/checker.py",
        "cwltool/command_line_tool.py",
        # "cwltool/context.py",  # monkeypatching
        "cwltool/cwlrdf.py",
        "cwltool/docker_id.py",
        "cwltool/docker.py",
        "cwltool/udocker.py",
        "cwltool/errors.py",
        "cwltool/executors.py",
        "cwltool/expression.py",
        "cwltool/factory.py",
        "cwltool/flatten.py",
        # "cwltool/__init__.py",
        "cwltool/job.py",
        "cwltool/load_tool.py",
        # "cwltool/loghandler.py",  # so we can monkeypatch the logger from tests
        # "cwltool/__main__.py",
        "cwltool/main.py",
        "cwltool/mutation.py",
        "cwltool/pack.py",
        # "cwltool/pathmapper.py",  # class PathMapper needs to be subclassable
        "cwltool/process.py",
        "cwltool/procgenerator.py",
        # "cwltool/provenance.py",  # WritableBag is having issues
        "cwltool/resolver.py",
        # "cwltool/sandboxjs.py",  # probably not speed critical, tests need to mock components
        "cwltool/secrets.py",
        "cwltool/singularity.py",
        "cwltool/software_requirements.py",
        # "cwltool/stdfsaccess.py",  # StdFsAccess needs to be subclassable
        "cwltool/subgraph.py",
        "cwltool/update.py",
        "cwltool/utils.py",
        "cwltool/validate_js.py",
        "cwltool/workflow.py",
    ]

    from mypyc.build import mypycify

    opt_level = os.getenv("MYPYC_OPT_LEVEL", "3")
    ext_modules = mypycify(mypyc_targets, opt_level=opt_level)
else:
    ext_modules = []

setup(
    name="cwltool",
    version="3.1",
    description="Common workflow language reference implementation",
    long_description=open(README).read(),
    long_description_content_type="text/x-rst",
    author="Common workflow language working group",
    author_email="common-workflow-language@googlegroups.com",
    url="https://github.com/common-workflow-language/cwltool",
    download_url="https://github.com/common-workflow-language/cwltool",
    ext_modules=ext_modules,
    # platforms='',  # empty as is conveyed by the classifier below
    # license='',  # empty as is conveyed by the classifier below
    packages=["cwltool", "cwltool.tests"],
    package_dir={"cwltool.tests": "tests"},
    include_package_data=True,
    install_requires=[
        "setuptools",
        "requests >= 2.6.1",  # >= 2.6.1 to workaround
        # https://github.com/ionrock/cachecontrol/issues/137
        "ruamel.yaml >= 0.15, < 0.17.21",
        "rdflib >= 4.2.2, < 6.2.0",
        "shellescape >= 3.4.1, < 3.9",
        "schema-salad >= 8.2.20211104054942, < 9",
        "mypy-extensions",
        "psutil >= 5.6.6",
        "prov == 1.5.1",
        "bagit >= 1.6.4",
        "typing-extensions",
        "coloredlogs",
        "pydot >= 1.4.1",
        "pyparsing != 3.0.2",  # breaks --print-dot (pydot) https://github.com/pyparsing/pyparsing/issues/319
        "argcomplete",
    ],
    extras_require={
        "deps": ["galaxy-tool-util >= 21.1.0"],
    },
    python_requires=">=3.7, <4",
    setup_requires=PYTEST_RUNNER,
    test_suite="tests",
    tests_require=[
        "pytest >= 6.2, < 6.3",
        "mock >= 2.0.0",
        "pytest-mock >= 1.10.0",
        "arcp >= 0.2.0",
        "rdflib-jsonld >= 0.4.0",
    ],
    entry_points={"console_scripts": ["cwltool=cwltool.main:run"]},
    zip_safe=True,
    cmdclass={"egg_info": Tagger},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: System :: Distributed Computing",
        "Topic :: Utilities",
    ],
)
