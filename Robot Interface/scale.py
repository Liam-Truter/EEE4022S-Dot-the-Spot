from opentrons import robot, instruments, containers
from opentrons.util.vector import Vector
import numpy as np
from weight_reader import Weight_reader

class Scale:
    def __init__(self):
        self.force_threshold = 0.5
        self.z_clearance = 5
    def start(self):
        self.weight_reader = Weight_reader()
        self.weight_reader.connect()
    def calibrate(self, point: Vector):
        self.point = point
    def move_to(self, coord, corner=False, arc=True):
        x_corn = self.point['x']
        y_corn = self.point['y']
        z_corn = self.point['z'] + self.z_clearance
        if corner:
            x_offset = 15
            y_offset = 15
            match coord:
                case 0:
                    x_corn += x_offset
                    y_corn += y_offset
                case 1:
                    x_corn += 122-x_offset
                    y_corn += y_offset
                case 2:
                    x_corn += 122-x_offset
                    y_corn += 122-y_offset
                case 3:
                    x_corn += x_offset
                    y_corn += 122-y_offset
                case 4:
                    x_corn += 61
                    y_corn += 61
        else:
            x_padding = (122-9*7)/2
            y_padding = (122-9*11)/2
            x_corn += x_padding + 9 * coord[0]
            y_corn += y_padding + 9 * coord[1]
        if arc:
            robot.move_head(z=100)
            robot.move_head(x=x_corn, y=y_corn)
            robot.move_head(z=z_corn)
        else:
            robot.move_head(x=x_corn,y=y_corn,z=z_corn)
    def find_depth(self, coord, corner=False, arc=False):
        self.move_to(coord, corner, arc)

        z_corn = self.point['z'] + self.z_clearance

        while True:
            weight = self.weight_reader.get_weight()
            net_weight = weight-self.natural_weight
            robot_pos = robot._driver.get_head_position()['current']
            robot_z = robot_pos['z']
            if net_weight > self.force_threshold:
                robot.move_head(z=z_corn)
                return robot_pos
            robot.move_head(z=robot_z-0.1)

    def touch_corners(self):
        self.coords = np.zeros((4,3))
        self.natural_weight = self.weight_reader.get_weight()
        for i in range(4):
            coord = self.find_depth(i, True, arc=i==0)
            self.coords[i,:] = np.array(coord.to_tuple())
            while self.weight_reader.get_weight() > self.natural_weight + self.force_threshold/5:
                pass
    
    def make_plane(self, clearance = 1.3):
        X = self.coords[:,0]
        Y = self.coords[:,1]
        Z = self.coords[:,2]

        A = np.vstack([X,Y, np.ones(len(X))]).T
        B = Z

        coefficients, residuals, _, _ = np.linalg.lstsq(A,B,rcond=None)

        a, b, d = coefficients

        self.x = np.linspace(self.point['x'] + 29.5, self.point['x'] + 122-29.5, 8)
        self.y = np.linspace(self.point['y'] + 11.5, self.point['y'] + 122-11.5, 12)

        # Heights of the plane in the z-axis
        self.z = np.zeros((8,12))
        # Coordinates of the well points
        self.points = np.zeros((8,12,3))
        self.rel_points = np.zeros_like(self.points)

        for i in range(8):
            for j in range(12):
                # z = ax + by + d + clearance
                self.z[i][j] = a*self.x[i] + b*self.y[j] + d + clearance
                # Coordinate of well point at row, column
                self.points[i][j] = np.array([self.x[i], self.y[j], self.z[i][j]])
                self.rel_points = self.points - np.array(self.point.to_tuple())
    
    def spot_to(self, coord):
        self.move_to(coord)
        robot.move_head(z=self.z[coord[0]][coord[1]])

    def save_coords(self):
        np.save("POINTS.npy", self.points)
    
    def load_coords(self):
        self.points = np.load("POINTS.npy")
        return self.points

def main():
    scale = Scale()
    if len(robot.get_serial_ports_list()) > 0:
        robot.connect(robot.get_serial_ports_list()[0])
    else:
        robot.connect("Virtual Smoothie")

    robot.home()

    corner_point = Vector(233.00, 0.00, -5.00)
    scale.calibrate(corner_point)

    scale.touch_corners()

    print()

if __name__ == '__main__':
    main()