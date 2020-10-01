"""Registry entries."""

from typing import List, Dict


class LocalRegistryEntry:
    """Local registry entry."""

    _index: str = None
    _fields: List[str] = []

    def __init__(self, **kwargs):
        """Initialize."""
        self._kwargs = kwargs

    @property
    def index(self):
        """Get index member value."""
        if self._index is not None:
            return getattr(self, self._index)

        return None

    @classmethod
    def get_index_name(cls) -> str:
        """Get index member name."""
        return cls._index

    @classmethod
    def get_field_names(cls) -> List[str]:
        """Get fields."""
        return cls._fields

    @property
    def serialized(self) -> Dict:
        """Get serialized."""
        serialized = {arg: getattr(self, arg) for arg in self._fields}
        serialized.update(self._kwargs)
        return serialized

    def __eq__(self, other):
        """Equal operator."""
        if not isinstance(other, LocalRegistryEntry):
            raise TypeError("unmatching time in comparison")

        for field in self._fields:
            this_value = getattr(self, field)
            other_value = getattr(other, field)
            if this_value != other_value:
                return False

        return True

    def __hash__(self, other):
        """Hash function."""
        field_values = tuple([getattr(self, field) for field in self._fields])
        return hash(field_values)

    def compare_entries(self, other):
        """Compare entries."""
        if not isinstance(other, LocalRegistryEntry):
            raise TypeError("unmatching type in comparison")

        modified_fields = {}
        for field in self._fields:
            this_value = getattr(self, field)
            other_value = getattr(other, field)
            if this_value != other_value:
                modified_fields[field] = (this_value, other_value)

        return modified_fields
