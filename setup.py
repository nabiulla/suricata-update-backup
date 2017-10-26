from setuptools import setup

import suricata

setup(
    name="suricata-updater",
    version=suricata.version,
    description="Suricata Update Tool",
    author="Jason Ish",
    author_email="ish@unx.ca",
    packages=[
        "suricata",
        "suricata.updater",
        "suricata.updater.rulecat",
        "suricata.updater.rulecat.configs",
        "suricata.updater.scripts",
        "suricata.updater.compat",
        "suricata.updater.compat.argparse",
    ],
    url="https://github.com/jasonish/suricata-updater",
    license="BSD",
    classifiers=[
        'License :: OSI Approved :: BSD License',
    ],
    scripts = [
        "bin/suricata-update",
    ],
)
