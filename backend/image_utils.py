"""
image_utils.py
==============
Reserved for future expansion of GovForm Automator.

Photo and signature upload were intentionally left OUT of this release
(per project requirements: physical photo/signature affixing after
printing). This module is kept as a placeholder so the documented project
structure stays stable, and so a future version can reintroduce image
handling (e.g. embedding a passport photo or scanned proof document)
without restructuring the backend.

Example of how this module would be used in a future version:

    from PIL import Image

    def fit_image_into_box(image_path: str, box_w_pt: float, box_h_pt: float):
        '''Resize an uploaded image to fit inside a PDF box while
        maintaining aspect ratio, returning the resized PIL Image.'''
        img = Image.open(image_path)
        img.thumbnail((box_w_pt * 4, box_h_pt * 4))  # 4x for print quality
        return img

No functions in this module are currently called by app.py or
pdf_generator.py.
"""
