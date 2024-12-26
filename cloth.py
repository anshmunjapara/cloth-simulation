import math

from object import Point, Stick
# from CoreMotion import CMMotionManager
import time


class Cloth:
    def __init__(self):
        self.force = {"x": 0, "y": 9.81}
        self.drag = 0.01
        self.elasticity = 10
        self.points = []
        self.sticks = []

        # self.motion_manager = CMMotionManager.alloc().init()
        #
        # # Use the motion manager
        # if self.motion_manager.isDeviceMotionAvailable():
        #     self.motion_manager.startDeviceMotionUpdates()
        #     time.sleep(1)
        #     motion_data = self.motion_manager.deviceMotion()
        #     print(motion_data)
        #     self.motion_manager.stopDeviceMotionUpdates()
        # else:
        #     print("Device motion not available")

    #
    # def update_force(self):
    #     if self.motion_manager.deviceMotion():
    #         attitude = self.motion_manager.deviceMotion().attitude()
    #         roll = attitude.roll  # Left/Right tilt
    #         pitch = attitude.pitch  # Forward/Backward tilt
    #
    #         # Map tilt to force values
    #         self.force["x"] = roll * 9.81  # Adjust scaling as needed
    #         self.force["y"] = pitch * 9.81 + 9.81  # Add gravity
    #         print(self.force)

    def setup(self, cols, rows, spacing, start_x, start_y):
        for y in range(rows):
            for x in range(cols):
                point = Point(start_x + x * spacing, start_y + y * spacing, 0.01, False)

                if x != 0:
                    leftPoint = self.points[len(self.points) - 1]
                    s = Stick(point, leftPoint, spacing)
                    leftPoint.add_stick(s, 0)
                    point.add_stick(s, 0)
                    self.sticks.append(s)

                if y != 0:
                    upPoint = self.points[x + (y - 1) * cols]
                    s = Stick(point, upPoint, spacing)
                    upPoint.add_stick(s, 1)
                    point.add_stick(s, 1)
                    self.sticks.append(s)

                if y == 0 and ((x == 0) or (x == cols - 1) or (x == (cols - 1) / 2)):
                    point.pinned = True

                self.points.append(point)

    def update(self, dt, mouse_pos, mouse_pos_rel, btn_clicked, radius, speed, fan):

        angle_rad = math.radians(-fan.angle+90)  # Convert angle to radians

        self.force["x"] = speed * math.sin(angle_rad)
        self.force["y"] = speed * math.cos(angle_rad) + 9.81
        for point in self.points:
            point.update(dt, self.force, 0.01, 10, mouse_pos, mouse_pos_rel, btn_clicked, radius)

        for _ in range(4):
            for stick in self.sticks:
                stick.update()
            for point in self.points:
                point.constrain()

    #     void Draw(Renderer* renderer) const;
    def draw(self, screen):
        for stick in self.sticks:
            stick.render(screen)

    # def stop_motion_updates(self):
    #     if self.motion_manager.isDeviceMotionAvailable():
    #         self.motion_manager.stopDeviceMotionUpdates()
