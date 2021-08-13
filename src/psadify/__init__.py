# idea taken from https://stackoverflow.com/a/47391252

import pkg_resources
import distutils.dist
import io

distribution = pkg_resources.get_distribution('psadify')
metadata_str = distribution.get_metadata(distribution.PKG_INFO)
metadata_obj = distutils.dist.DistributionMetadata()
metadata_obj.read_pkg_file(io.StringIO(metadata_str))

__author__ = metadata_obj.author 
__email__ = metadata_obj.author_email 
__version__ = metadata_obj.version 