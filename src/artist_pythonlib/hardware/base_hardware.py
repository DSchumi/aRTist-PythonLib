# Copyright 2023 Simon Wittl (Deggendorf Institute of Technology)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

from ..remote_connection import Junction, _rc
from ..api import API


class BaseHardware:
    def __init__(self, remote_control: Junction | API = None) -> None:
        if isinstance(remote_control, Junction):
            self.rc = remote_control
        elif isinstance(remote_control, API):
            self.rc = remote_control.rc
        elif remote_control is None:
            self.rc = _rc
        else:
            raise ValueError("Wrong remote_control argument?")
