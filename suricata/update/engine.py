# Copyright (C) 2017 Open Information Security Foundation
#
# You can copy, redistribute or modify this Program under the terms of
# the GNU General Public License version 2 as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# version 2 along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

# Copyright (c) 2015 Jason Ish
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# This module contains functions for interacting with the Suricata
# application (aka the engine).

from __future__ import print_function

import os
import os.path
import subprocess
import re
import logging
from collections import namedtuple

logger = logging.getLogger()

SuricataVersion = namedtuple(
    "SuricataVersion", ["major", "minor", "patch", "full", "short", "raw"])

def get_path(program="suricata"):
    """Find Suricata in the shell path."""
    for path in os.environ["PATH"].split(os.pathsep):
        if not path:
            continue
        suricata_path = os.path.join(path, program)
        logger.debug("Testing path: %s" % (path))
        if os.path.exists(suricata_path):
            logger.debug("Found %s." % (path))
            return suricata_path
    return None

def parse_version(buf):
    m = re.search("((\d+)\.(\d+)(\.(\d+))?(\w+)?)", str(buf).strip())
    if m:
        full = m.group(1)
        major = int(m.group(2))
        minor = int(m.group(3))
        if not m.group(5):
            patch = 0
        else:
            patch = int(m.group(5))
        short = "%s.%s" % (major, minor)
        return SuricataVersion(
            major=major, minor=minor, patch=patch, short=short, full=full,
            raw=buf)
    return None

def get_version(path=None):
    """Get a SuricataVersion named tuple describing the version.

    If no path argument is found, the envionment PATH will be
    searched.
    """
    if not path:
        path = get_path("suricata")
    if not path:
        return None
    output = subprocess.check_output([path, "-V"])
    if output:
        return parse_version(output)
    return None

def test_configuration(path, rule_filename=None):
    """Test the Suricata configuration with -T."""
    test_command = [
        path,
        "-T",
        "-l", "/tmp",
    ]
    if rule_filename:
        test_command += ["-S", rule_filename]

    # This makes the Suricata output look just like suricata-udpate
    # output.
    env = {
        "SC_LOG_FORMAT": "%t - <%d> -- ",
        "SC_LOG_LEVEL": "Warning",
    }

    rc = subprocess.Popen(test_command, env=env).wait()
    if rc == 0:
        return True
    return False
