"""
Provides the HUD data system used by the COSMOS Engine.

The HUD stores simulation information that can be displayed by
the rendering system. It does not perform any rendering.

Author: Neil
Project: COSMOS
"""


class HUD:
    """
    Stores information to be displayed by the COSMOS HUD.
    """

    def __init__(self) -> None:
        """
        Creates an empty HUD.
        """

        self.data: dict[str, object] = {}

    def set(self, label: str, value: object) -> None:
        """
        Adds or updates a HUD entry.
        """

        self.data[label] = value

    def remove(self, label: str) -> None:
        """
        Removes a HUD entry if it exists.
        """

        self.data.pop(label, None)

    def clear(self) -> None:
        """
        Removes all HUD entries.
        """

        self.data.clear()

    def get_data(self) -> dict[str, object]:
        """
        Returns the current HUD data.
        """

        return self.data.copy()