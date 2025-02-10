"""Publish UDIM tiles."""
import re

import pyblish.api
from ayon_core.lib import BoolDef
from ayon_core.pipeline import publish

UDIM_REGEX = re.compile(r"(.*)[._](?P<udim>\d{4})\.(.*)")


class CollectUDIMs(
    pyblish.api.InstancePlugin, publish.AYONPyblishPluginMixin):
    """Collect UDIMs tiles."""

    label = "Collect UDIMs"
    order = pyblish.api.CollectorOrder + 0.499
    families = ["texture"]



    def process(self, instance):
        # type: (pyblish.api.Instance) -> None
        instance_settings = self.get_attr_values_from_data(instance.data)
        is_udim = instance_settings.get("isUDIM", False)
        if not is_udim:
            return

        representations = instance.data["representations"]
        first_repr = representations[0]        

        # Check that all files have same staging dir
        if not all(r["stagingDir"] == first_repr["stagingDir"] for r in representations):
            raise ValueError(f"Files not from the same directory")

        new_repr = {}
        # Copy ext, name, tags to new repr
        for key in ["ext","name","tags","stagingDir"]:
            new_repr[key] = first_repr.get(key)

        # Add files to new repr
        new_repr["files"] = []
        new_repr["udim"] = []
        for representation in instance.data["representations"]:
            file = representation["files"]
            if isinstance(file, (list, tuple)):
                continue
            
            # sourcery skip: use-named-expression
            match = re.search(UDIM_REGEX, file)
            if match:
                new_repr["files"].append(file)
                new_repr["udim"].append(match.group("udim"))

        instance.data["representations"] = [new_repr]
        

    @classmethod
    def get_attribute_defs(cls):
        return [
            BoolDef("isUDIM",
                    label="Is UDIM",
                    default=False)
        ]