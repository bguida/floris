# Copyright 2021 NREL

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# See https://floris.readthedocs.io for documentation


import matplotlib.pyplot as plt
import numpy as np

import floris.tools.visualization as wakeviz
from floris.tools import FlorisInterface


"""
This example initializes the FLORIS software, and then uses internal
functions to run a simulation and plot the results. In this case,
we are plotting three slices of the resulting flow field:
1. Horizontal slice parallel to the ground and located at the hub height
2. Vertical slice of parallel with the direction of the wind
3. Veritical slice parallel to to the turbine disc plane

Additionally, an alternative method of plotting a horizontal slice
is shown. Rather than calculating points in the domain behind a turbine,
this method adds an additional turbine to the farm and moves it to
locations throughout the farm while calculating the velocity at it's
rotor.
"""

# Initialize FLORIS with the given input file via FlorisInterface.
# For basic usage, FlorisInterface provides a simplified and expressive
# entry point to the simulation routines.
fi = FlorisInterface("inputs/gch.yaml")

# turbine layout
fi.reinitialize(layout_x=[4079.8,5080.3,4755.8,4458.4,4137.6,3808.8,
3499.8,3797.8,3457.7,3162.6,2873.9,3843.9,4153.2,4454.5,4781.5,
5078.8,1910.6,1606.0,1296.7,2569.4,2880.4,3186.6,1032.6,50.0,
386.2,703.7,1001.5,3881.8,2606.4,1333.7,1636.7,1961.7,2245.8,
5768.9,4188.0,2918.2,4480.5,3221.9,3546.1,5159.9,5472.7,7045.8,
7364.0,6094.4,4825.0,8335.0,8635.6,8944.1,9252.0,9554.2,9855.6,
9592.8,11175.8,9894.9,11477.9,10215.3,11798.3,10526.0,12109.0,
10829.8,12412.8,11135.0,5113.0,6397.1,7671.9,7991.9,6705.6,
5424.8,5751.5,7013.3,8281.1,8582.0,7321.7,6055.3,12729.4,11476.4,
10196.2,8917.3,9228.8,6368.9,7636.2,7948.0,8251.8,7309.4,7019.2,
5763.0,6673.4,6995.4,5710.1,6032.5
], 
layout_y=[19844.7,20331.2,18929.7,17503.5,16076.9,14681.2,
13255.8,18486.8,17076.2,15620.6,14209.6,7994.2,9389.5,10808.1,
12229.5,13648.8,12846.9,11401.6,10034.3,9027.8,10419.9,11826.9,
1887.5,4332.4,5775.6,7191.3,8646.9,1265.6,2288.7,3306.7,4742.8,
6191.0,7571.6,3082.3,2667.8,3686.1,4113.7,5135.7,6549.4,263.4,
1703.2,2069.1,3497.7,4496.1,5565.5,1056.3,2480.8,3893.4,5313.5,
6747.8,8180.2,50.0,464.6,1457.4,1872.0,2875.1,3289.7,4292.2,
4706.8,5706.0,6120.6,7125.8,6950.6,5942.3,4953.3,6359.1,7384.0,
8383.5,9805.0,8761.0,7763.6,9166.6,10219.4,11215.5,7557.3,8590.9,
9603.2,10652.3,12065.5,12654.0,11661.9,13086.6,14482.8,16943.4,
19356.9,15271.3,14063.2,15506.9,16523.6,17928.6
])


# The rotor plots show what is happening at each turbine, but we do not
# see what is happening between each turbine. For this, we use a
# grid that has points regularly distributed throughout the fluid domain.
# The FlorisInterface contains functions for configuring the new grid,
# running the simulation, and generating plots of 2D slices of the
# flow field.

# Note this visualization grid created within the calculate_horizontal_plane function will be reset
# to what existed previously at the end of the function

# Using the FlorisInterface functions, get 2D slices.
horizontal_plane = fi.calculate_horizontal_plane(
    x_resolution=200,
    y_resolution=100,
    height=90.0,
    # yaw_angles=np.array([[[25.,0.,0.,0]]]),
)

y_plane = fi.calculate_y_plane(
    x_resolution=200,
    z_resolution=100,
    crossstream_dist=7800.0,
    # yaw_angles=np.array([[[25.,0.,0.,0]]]),
)
cross_plane = fi.calculate_cross_plane(
    y_resolution=100,
    z_resolution=100,
    downstream_dist=630.0,
    # yaw_angles=np.array([[[25.,0.,0.,0]]]),
)

# Create the plots
fig, ax_list = plt.subplots(3, 1, figsize=(10, 8))
ax_list = ax_list.flatten()
wakeviz.visualize_cut_plane(
    horizontal_plane,
    ax=ax_list[0],
    label_contours=True,
    title="Horizontal"
)
wakeviz.visualize_cut_plane(
    y_plane,
    ax=ax_list[1],
    label_contours=True,
    title="Streamwise profile"
)
wakeviz.visualize_cut_plane(
    cross_plane,
    ax=ax_list[2],
    label_contours=True,
    title="Spanwise profile"
)

# FLORIS further includes visualization methods for visualing the rotor plane of each
# Turbine in the simulation

# # Run the wake calculation to get the turbine-turbine interfactions
# # on the turbine grids
# fi.calculate_wake()



# FLORIS supports multiple types of grids for capturing wind speed
# information. The current input file is configured with a square grid
# placed on each rotor plane with 9 points in a 3x3 layout. For visualization,
# this resolution can be increased.  Note this operation, unlike the
# calc_x_plane above operations does not automatically reset the grid to
# the initial status as definied by the input file

# Increase the resolution of points on each turbien plane
solver_settings = {
    "type": "turbine_grid",
    "turbine_grid_points": 10
}
fi.reinitialize(solver_settings=solver_settings)


# Set the wind direction to run 360 degrees
# wd_array = np.arange(0, 360, 1)
fi.reinitialize( wind_speeds=[16.0] )

# insert virual metmast locations
# points_x = np.arange(0,20400,100)
# points_y = np.arange(0,20400,100)
# points_z =  [10] * 204

nx, ny = (2, 1)
x = np.linspace(0, 13000, nx)
y = np.linspace(0, 20000, ny)
points_xg, points_yg = np.meshgrid(x, y)
# points_z = np.full((nx, ny), 11)

points_x=np.reshape(points_xg,nx*ny)
points_y=np.reshape(points_yg,nx*ny)
points_z = points_x*0+10

# Collect the points
u_at_points = fi.sample_flow_at_points(points_x, points_y, points_z)
print(fi.floris.flow_field.u_sorted)
print(fi.floris.flow_field.v_sorted)
# print(fi.sample_flow_at_points.v_sorted)
# print(u_at_points)
wait = input("Press Enter to continue.")

fig, ax = plt.subplots(1,2)
fig.set_size_inches(10,4)

ax[0].scatter(points_x, points_y, color="red", marker="x", label="Met mast")
ax[0].grid()
ax[0].set_xlabel("x [m]")
ax[0].set_ylabel("y [m]")
ax[0].legend()

# Plot the velocities
# for z_idx, z in enumerate(points_z):
    # ax[1].plot(wd_array, u_at_points[:, :, z_idx].flatten(), label=f'Speed at z={z} m')
# ax[1].grid()
# ax[1].legend()
# ax[1].set_xlabel('Wind Direction (deg)')
# ax[1].set_ylabel('Wind Speed (m/s)')

plt.show()

