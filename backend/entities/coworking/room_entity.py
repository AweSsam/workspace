"""Entity for Room."""

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from ...models.coworking import Room, RoomDetails
from ...models.coworking.room_details import ExtendedRoomDetails
from typing import Self

__authors__ = ["Sameera & Dharshini"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class RoomEntity(EntityBase):
    """Entity for Rooms under XL management."""

    __tablename__ = "coworking__room"

    # Room Model Fields
    id: Mapped[str] = mapped_column(String, primary_key=True)
    capacity: Mapped[int] = mapped_column(Integer, index=True)
    # RoomDetails Model Fields Follow
    building: Mapped[str] = mapped_column(String)
    room: Mapped[str] = mapped_column(String)
    nickname: Mapped[str] = mapped_column(String)
    reservable: Mapped[bool] = mapped_column(Boolean)

    seats: Mapped[list["SeatEntity"]] = relationship(  # type: ignore
        "SeatEntity", back_populates="room"
    )

    has_projector: Mapped[bool] = mapped_column(Boolean)
    has_whiteboard: Mapped[bool] = mapped_column(Boolean)
    has_monitor: Mapped[bool] = mapped_column(Boolean)

    def to_model(self) -> Room:
        """Converts the entity to a model.

        Returns:
            Room: The model representation of the entity."""
        return Room(id=self.id, nickname=self.nickname)

    def to_details_model(self) -> RoomDetails:
        """Converts the entity to a RoomDetail model.

        Returns:
            RoomDetails: The model representation of the entity."""
        return RoomDetails(
            id=self.id,
            nickname=self.nickname,
            building=self.building,
            room=self.room,
            capacity=self.capacity,
            reservable=self.reservable,
            seats=[seat.to_model() for seat in self.seats],
        )

    def to_extended_details_model(self) -> ExtendedRoomDetails:
        """Converts the entity to an ExtendedRoomDetails model.

        Returns:
            ExtendedRoomDetails: The model representation of the entity."""
        return ExtendedRoomDetails(
            id=self.id,
            nickname=self.nickname,
            building=self.building,
            room=self.room,
            capacity=self.capacity,
            reservable=self.reservable,
            seats=[seat.to_model() for seat in self.seats],
            has_projector=self.has_projector,
            has_whiteboard=self.has_whiteboard,
            has_monitor=self.has_monitor,
        )

    @classmethod
    def from_model(cls, model: ExtendedRoomDetails) -> Self:
        """Create an RoomEntity from a Room model.

        Args:
            model (Room): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted)."""
        return cls(
            id=model.id,
            nickname=model.nickname,
            building=model.building,
            room=model.room,
            capacity=model.capacity,
            reservable=model.reservable,
            seats=model.seats,
            has_projector=model.has_projector,
            has_whiteboard=model.has_whiteboard,
            has_monitor=model.has_monitor,
        )
