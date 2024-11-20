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

from pathlib import Path

from artist_pythonlib import API, PROJECTIONGEOMETRIES
from artist_pythonlib.trajectory import circular_trajectory


NUMBER_OF_PROJECTIONS = 20
SAVEFOLDER = Path('./workspace') / 'example_02'
SAVEFOLDER.mkdir(exist_ok=True)


def main():
    trajectory = circular_trajectory(500., 1000., NUMBER_OF_PROJECTIONS)
    api = API()

    for i in range(NUMBER_OF_PROJECTIONS):
        source, detector, rotation_matrix = trajectory[0][i], trajectory[1][i], trajectory[2][i]
        
        api.translate('S', *source)
        api.translate('D', *detector)
        api.rotate_from_rotation_matrix('S', rotation_matrix)
        api.rotate_from_rotation_matrix('D', rotation_matrix)

        api.save_image(SAVEFOLDER / f'{i:03}.tif', save_projection_geometry=PROJECTIONGEOMETRIES.THD)


if __name__ == '__main__':
    main()
    