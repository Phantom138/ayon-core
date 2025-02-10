"""
Collector for custom "texture" prodcut

Since the product doesn't really exist, and is only used for prettier names, i have to change it back to an "image" product.

A bit hacky but it should work
"""

import pyblish.api
from ayon_core.lib import BoolDef
from ayon_core.pipeline import publish

class CollectTexture(
    pyblish.api.InstancePlugin, publish.AYONPyblishPluginMixin):
    """Convert texture to Image"""

    label = "Collect Texture (convert to image)"
    order = pyblish.api.CollectorOrder + 0.4995
    families = ["texture"]


    def process(self, instance):
        # self.log.debug(repr(instance))
        new_family = "image"
        instance.data["family"] = new_family
        instance.data["productType"] = new_family
        instance.data["families"] = [new_family]
        instance.data["anatomyData"]["family"] = new_family
        instance.data["anatomyData"]["product"]["type"] = new_family

        