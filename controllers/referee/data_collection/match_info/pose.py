from dataclasses import dataclass
from typing import Tuple

import transforms3d


@dataclass(frozen=True)
class Position:
    """Position of an object in 3D space.

    :param x: X coordinate of the position
    :type x: float
    :param y: Y coordinate of the position
    :type y: float
    :param z: Z coordinate of the position
    :type z: float
    """

    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Rotation:
    """Rotation of an object in 3D space as a quaternion.

    :param x: X component of the quaternion
    :type x: float
    :param y: Y component of the quaternion
    :type y: float
    :param z: Z component of the quaternion
    :type z: float
    :param w: W component of the quaternion
    :type w: float
    """

    x: float
    y: float
    z: float
    w: float

    def quaternion(self) -> Tuple[float, float, float, float]:
        """Return the quaternion as a tuple.

        :return: Quaternion in the order [x, y, z, w]
        :rtype: Tuple[float, float, float, float]
        """
        return (self.x, self.y, self.z, self.w)

    def rpy(self) -> Tuple[float, float, float]:
        """Convert rotation to euler angles.

        :return: Euler angles in the order [roll, pitch, yaw]
        :rtype: Tuple[float, float, float]
        """
        return transforms3d.euler.quat2euler((self.x, self.y, self.z, self.w))


@dataclass(frozen=True)
class Pose:
    """Pose of an object in 3D space.

    :param position: Position of the object
    :type position: Position
    :param rotation: Rotation of the object
    :type rotation: Rotation
    """

    position: Position
    rotation: Rotation