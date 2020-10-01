"""Registry."""

from typing import Type, List
import json
import os


class RegistryError(Exception):
    """Generic registry error."""


class LocalRegistry:
    """Local registry."""

    def __init__(self, registry_name: str, entry_class: Type, db_path: str):
        """Initialize."""
        self._entry_class = entry_class

        self._registry_location = os.path.join(
            db_path, registry_name + ".json"
        )

        if not os.path.exists(self._registry_location):
            try:
                with open(self._registry_location, "w") as registry:
                    registry.write("[]")

            except OSError:
                raise RegistryError("cannot create registry")

        # load registry
        try:
            with open(self._registry_location, "r") as registry:
                _registry_contents = json.load(registry)
        except (OSError, json.JSONDecodeError):
            raise RegistryError("cannot load registry.")

        # build
        self._registry_contents = []
        self._initializing = True
        self.build_registry(_registry_contents)
        self._initializing = False

    @property
    def serialized(self):
        """Get serialized."""
        return [item.serialized for item in self._registry_contents]

    def update_registry(self, api_obj):
        """Update registry."""
        raise NotImplementedError

    def value_changed(self, entry_index, field_name, old_value, new_value):
        """Value changed callback."""

    def new_entry(self, content):
        """New entry callback."""

    def build_registry(self, contents: List):
        """Build registry."""
        new_registry_contents = []
        for item in contents:
            new_content = self._entry_class(**item)
            new_registry_contents.append(new_content)
            try:
                index_key = self._entry_class.get_index_name()
                if index_key is not None:
                    index_value = item[index_key]
                    if not self._initializing and index_value not in self:
                        # new content
                        self.new_entry(new_content)
                    current_content = self[index_value]
                    if (
                        not self._initializing
                        and current_content != new_content
                    ):
                        modified_fields = current_content.compare_entries(
                            new_content
                        )
                        for (
                            field_name,
                            (old_value, new_value),
                        ) in modified_fields.items():
                            self.value_changed(
                                index_value, field_name, old_value, new_value
                            )
            except KeyError:
                pass
        # self._registry_contents = [
        #     self._entry_class(**item) for item in contents
        # ]
        self._registry_contents = new_registry_contents

    def commit_registry(self):
        """Commit to disk."""
        with open(self._registry_location, "w") as registry:
            json.dump(self.serialized, registry, indent=2)

    def __getitem__(self, item):
        if self._entry_class.get_index_name() is not None:
            for element in self._registry_contents:
                if element.index == item:
                    return element

        raise KeyError

    def __iter__(self):
        """Get iterator."""
        return iter(self._registry_contents)

    def __contains__(self, item):
        """Contains or not."""
        try:
            _ = self[item]
            return True
        except KeyError:
            return False

    @property
    def data_layout(self):
        """Get data layout."""
        return self._entry_class.get_field_names()
