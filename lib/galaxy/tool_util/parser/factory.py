"""Constructors for concrete tool and input source objects."""
from __future__ import absolute_import

import logging
from collections import OrderedDict

import yaml

from galaxy.tool_util.loader import load_tool_with_refereces
from .cwl import CwlToolSource
from .interface import InputSource
from .xml import XmlInputSource, XmlToolSource
from .yaml import YamlToolSource
from ..fetcher import ToolLocationFetcher

log = logging.getLogger(__name__)


def get_tool_source(config_file=None, xml_tree=None, enable_beta_formats=True, tool_location_fetcher=None):
    """Return a ToolSource object corresponding to supplied source.

    The supplied source may be specified as a file path (using the config_file
    parameter) or as an XML object loaded with load_tool_with_refereces.
    """
    if xml_tree is not None:
        return XmlToolSource(xml_tree, source_path=config_file)
    elif config_file is None:
        raise ValueError("get_tool_source called with invalid config_file None.")

    if tool_location_fetcher is None:
        tool_location_fetcher = ToolLocationFetcher()

    config_file = tool_location_fetcher.to_tool_path(config_file)
    if not enable_beta_formats:
        tree, macro_paths = load_tool_with_refereces(config_file)
        return XmlToolSource(tree, source_path=config_file, macro_paths=macro_paths)

    if config_file.endswith(".yml"):
        log.info("Loading tool from YAML - this is experimental - tool will not function in future.")
        with open(config_file, "r") as f:
            as_dict = ordered_load(f)
            return YamlToolSource(as_dict, source_path=config_file)
    elif config_file.endswith(".json") or config_file.endswith(".cwl"):
        log.info("Loading CWL tool - this is experimental - tool likely will not function in future at least in same way.")
        return CwlToolSource(config_file)
    else:
        tree, macro_paths = load_tool_with_refereces(config_file)
        return XmlToolSource(tree, source_path=config_file, macro_paths=macro_paths)


def ordered_load(stream):
    class OrderedLoader(yaml.Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)

    return yaml.load(stream, OrderedLoader)


def get_tool_source_from_representation(tool_format, tool_representation):
    # TODO: make sure whatever is consuming this method uses ordered load.
    log.info("Loading dynamic tool - this is experimental - tool may not function in future.")
    if tool_format == "GalaxyTool":
        if "version" not in tool_representation:
            tool_representation["version"] = "1.0.0"  # Don't require version for embedded tools.
        return YamlToolSource(tool_representation)
    else:
        raise Exception("Unknown tool representation format [%s]." % tool_format)


def get_input_source(content):
    """Wrap an XML element in a XmlInputSource if needed.

    If the supplied content is already an InputSource object,
    it is simply returned. This allow Galaxy to uniformly
    consume using the tool input source interface.
    """
    if not isinstance(content, InputSource):
        content = XmlInputSource(content)
    return content


__all__ = ("get_tool_source", "get_input_source")