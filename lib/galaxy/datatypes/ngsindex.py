"""
NGS indexes
"""
import logging
import os

from .metadata import MetadataElement
from .text import Html

log = logging.getLogger(__name__)


class BowtieIndex(Html):
    """
    base class for BowtieIndex
    is subclassed by BowtieColorIndex and BowtieBaseIndex
    """
    MetadataElement(name="base_name", desc="base name for this index set", default='galaxy_generated_bowtie_index', set_in_upload=True, readonly=True)
    MetadataElement(name="sequence_space", desc="sequence_space for this index set", default='unknown', set_in_upload=True, readonly=True)

    composite_type = 'auto_primary_file'

    def generate_primary_file(self, dataset=None):
        """
        This is called only at upload to write the html file
        cannot rename the datasets here - they come with the default unfortunately
        """
        return '<html><head></head><body>AutoGenerated Primary File for Composite Dataset</body></html>'

    def regenerate_primary_file(self, dataset):
        """
        cannot do this until we are setting metadata
        """
        bn = dataset.metadata.base_name
        flist = os.listdir(dataset.extra_files_path)
        rval = ['<html><head><title>Files for Composite Dataset %s</title></head><p/>Comprises the following files:<p/><ul>' % (bn)]
        for fname in flist:
            sfname = os.path.split(fname)[-1]
            rval.append(f'<li><a href="{sfname}">{sfname}</a>')
        rval.append('</ul></html>')
        with open(dataset.file_name, 'w') as f:
            f.write("\n".join(rval))
            f.write('\n')

    def set_peek(self, dataset, is_multi_byte=False):
        if not dataset.dataset.purged:
            dataset.peek = "Bowtie index file (%s)" % (dataset.metadata.sequence_space)
            dataset.blurb = "%s space" % (dataset.metadata.sequence_space)
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def display_peek(self, dataset):
        try:
            return dataset.peek
        except Exception:
            return "Bowtie index file"


class BowtieColorIndex(BowtieIndex):
    """
    Bowtie color space index
    """
    MetadataElement(name="sequence_space", desc="sequence_space for this index set", default='color', set_in_upload=True, readonly=True)

    file_ext = 'bowtie_color_index'


class BowtieBaseIndex(BowtieIndex):
    """
    Bowtie base space index
    """
    MetadataElement(name="sequence_space", desc="sequence_space for this index set", default='base', set_in_upload=True, readonly=True)

    file_ext = 'bowtie_base_index'
