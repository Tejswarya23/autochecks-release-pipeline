import unittest
from vehicle_simulator.sensor import LidarSensor, CameraSensor

class TestLidarSensor(unittest.TestCase):

    #PASS CASES
    def test_read_returns_data(self):
        s = LidarSensor("lidar_01")
        data = s.read()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["sensor_id"], "lidar_01")

    def test_health_check_active(self):
        s = LidarSensor("lidar_02")
        self.assertTrue(s.health_check())

    def test_custom_range(self):
        s = LidarSensor("lidar_03", range_m=200.0)
        self.assertEqual(s.read()["range_m"], 200.0)

    def test_points_detected(self):
        s = LidarSensor("lidar_04")
        self.assertEqual(s.read()["points_detected"], 1024)

    #FAILURE CASES
    def test_offline_sensor_raises(self):
        s = LidarSensor("lidar_05")
        s.active = False
        with self.assertRaises(RuntimeError):
            s.read()

    def test_health_check_offline(self):
        s = LidarSensor("lidar_06")
        s.active = False
        self.assertFalse(s.health_check())


class TestCameraSensor(unittest.TestCase):

    #PASS CASES
    def test_capture_returns_data(self):
        c = CameraSensor("cam_01")
        data = c.capture()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["frame_rate"], 30)

    def test_health_check_active(self):
        c = CameraSensor("cam_01")
        self.assertTrue(c.health_check())

    def test_custom_resolution(self):
        c = CameraSensor("cam_02", resolution="4K")
        self.assertEqual(c.capture()["resolution"], "4K")

    #FAILURE CASES
    def test_offline_camera_raises(self):
        c = CameraSensor("cam_03")
        c.active = False
        with self.assertRaises(RuntimeError):
            c.capture()

    def test_health_check_offline(self):
        c = CameraSensor("cam_04")
        c.active = False
        self.assertFalse(c.health_check())


if __name__ == "__main__":
    unittest.main(verbosity=2)
