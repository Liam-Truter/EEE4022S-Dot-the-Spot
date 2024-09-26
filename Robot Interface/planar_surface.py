import numpy as np
from opentrons import robot, instruments, containers
from opentrons.util.vector import Vector
import matplotlib.pyplot as plt

class PlanarSurface:
    def __init__(self):
        self.spacing = 8 # Spacing between points in mm
    def create_from_points(self, p1: Vector, p2: Vector, p3: Vector):
        spacing = self.spacing

        # Decompose vector values into arrays per axis
        x_vals = [p1['x'], p2['x'], p3['x']]
        y_vals = [p1['y'], p2['y'], p3['y']]
        z_vals = [p1['z'], p2['z'], p3['z']]

        # Bounds of the grid in the x-axis
        x_min = min(x_vals)
        x_max = max(x_vals)
        x_range = x_max - x_min
        x_grids = x_range // spacing
        x_pad = (x_range % spacing + spacing*(x_grids-8))/2
        self.x = np.linspace(x_min+x_pad, x_max-x_pad,8)

        # Bounds of the grid in the y-axis
        y_min = min(y_vals)
        y_max = max(y_vals)
        y_range = y_max - y_min
        y_grids = y_range // spacing
        y_pad = (y_range % spacing + spacing*(y_grids-12))/2
        self.y = np.linspace(y_min+y_pad, y_max-y_pad,12)

        # Get two coplanar vectors for planar eqn
        vp1 = np.array([p1['x'], p1['y'], p1['z']])
        vp2 = np.array([p2['x'], p2['y'], p2['z']])
        vp3 = np.array([p3['x'], p3['y'], p3['z']])
        v1 = vp1 - vp2
        v2 = vp2 - vp3

        # abcd coefficients (ax + by + cz = d)
        abc = np.cross(v1, v2)
        a = abc[0]
        b = abc[1]
        c = abc[2]
        d = np.dot(abc, vp1)

        # Heights of the plane in the z-axis
        self.z = np.zeros((8,12))
        # Coordinates of the well points
        self.points = np.zeros((8,12,3))

        for i in range(8):
            for j in range(12):
                # z = (d - ax - by)/c
                self.z[i][j] = (d - a*self.x[i] - b*self.y[j])/c
                # Coordinate of well point at row, column
                self.points[i][j] = np.array([self.x[i], self.y[j], self.z[i][j]])
    
    def wells(self, well: str) -> Vector:
        # Get row index
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        row = rows.index(well[0])

        # Get column index
        col = int(well[1:]) - 1

        # Return Vector of point at row, col
        return Vector(self.points[row,col,:])



def main():
    ps = PlanarSurface()

    p1 = Vector({'x': 215.00, 'y': 4.00, 'z': -46.50})
    p2 = Vector({'x': 285.00, 'y': 4.00, 'z': -48.30})
    p3 = Vector({'x': 285.00, 'y': 114.50, 'z': -51.50})

    ps.create_from_points(p1, p2, p3)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(ps.points[:,:,0],ps.points[:,:,1],ps.points[:,:,2])
    plt.show()
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    targets = []

    source_well_pos = Vector(227,240,15)
    p10 = instruments.Pipette(axis='b')
    for row in rows:
        for col in cols:
            targets.append(row + col)
    for i in range(10):
        robot.move_to(source_well_pos)
        for j in range(10):
            if 10*i + j < 96:
                pass


if __name__ == '__main__':
    main()