"""custom_1 dataset."""

import tensorflow_datasets as tfds
import os
import glob
import tensorflow as tf
import numpy as np
import io
import tifffile as tiff
import natsort
import random
# TODO(custom_1): Markdown description  that will appear on the catalog page.
_DESCRIPTION = """
Description is **formatted** as markdown.

It should also contain any processing which has been applied (if any),
(e.g. corrupted example skipped, images cropped,...):
"""

# TODO(custom_1): BibTeX citation
_CITATION = """
"""


class Custom0(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for cornell_grasp dataset."""

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  MANUAL_DOWNLOAD_INSTRUCTIONS = '/home/park/park/'

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    # TODO(cornell_grasp): Specifies the tfds.core.DatasetInfo object
    
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            # These are the features of your dataset like images, labels ...
            'rgb': tfds.features.Image(shape=(None, None, 3)),
            'mask': tfds.features.Image(shape=(None, None, 1)),
        }),
        # If there's a common (input, target) tuple from the
        # features, specify them here. They'll be used if
        # `as_supervised=True` in `builder.as_dataset`.
        # supervised_keys=('input', "depth", "box"),  # Set to `None` to disable
        supervised_keys=None,
        homepage='https://dataset-homepage/',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    # TODO(cornell_grasp): Downloads the data and defines the splits
    archive_path = dl_manager.manual_dir / 'data.zip'
    extracted_path = dl_manager.extract(archive_path)

    # TODO(cornell_grasp): Returns the Dict[split names, Iterator[Key, Example]]
    return {
        'train': self._generate_examples(img_path=extracted_path/'rgb', mask_path=extracted_path/'mask')
    }

  def _generate_examples(self, img_path, mask_path):
    img = os.path.join(img_path, '*.png')
    mask = os.path.join(mask_path, '*.png')
    
    img_files = glob.glob(img)
    # img_files.sort()
    img_files = natsort.natsorted(img_files,reverse=True)
    
    mask_files = glob.glob(mask)
    # mask_files.sort()
    mask_files = natsort.natsorted(mask_files,reverse=True)
    
  
    for i in range(len(img_files)):
      yield i, {
          'rgb': img_files[i],
          'mask' : mask_files[i]
      }

  def _load_tif(self, filename: str) -> np.ndarray:
    """Loads TIF file and returns as an image array in [0, 1]."""
    with tf.io.gfile.GFile(filename, "rb") as fid:
      # img = tfds.core.lazy_imports.skimage.external.tifffile.imread(
          # io.BytesIO(fid.read())).astype(np.float32)
      img = tiff.imread(io.BytesIO(fid.read())).astype(np.float32)
      img = np.expand_dims(img , axis=-1)
    # img = (img - min_per_channel) / (max_per_channel - min_per_channel) * 255
    # img = np.clip(img, 0, 255).astype(np.uint8)
    return img