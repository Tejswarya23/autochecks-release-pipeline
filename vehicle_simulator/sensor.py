"""Simulated AV sensor module - mimics lidar/camera data pipeline."""

class LidarSensor:
    def __init__(self, sensor_id: str, range_m: float = 100.0):
        self.sensor_id = sensor_id
        self.range_m = range_m
        self.active = True

    def read(self) -> dict:
        if not self.active:
            raise RuntimeError(f"Sensor {self.sensor_id} is offline")
        return {
            "sensor_id": self.sensor_id,
            "range_m": self.range_m,
            "status": "ok",
            "points_detected": 1024,
        }

    def health_check(self) -> bool:
        return self.active


class CameraSensor:
    def __init__(self, sensor_id: str, resolution: str = "1080p"):
        self.sensor_id = sensor_id
        self.resolution = resolution
        self.active = True

    def capture(self) -> dict:
        if not self.active:
            raise RuntimeError(f"Camera {self.sensor_id} is offline")
        return {
            "sensor_id": self.sensor_id,
            "resolution": self.resolution,
            "status": "ok",
            "frame_rate": 30,
        }

    def health_check(self) -> bool:
        return self.active
