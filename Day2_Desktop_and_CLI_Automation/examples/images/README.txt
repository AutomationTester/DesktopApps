Reference images for image-based automation (example 06_image_based_click.py)
=============================================================================

calc_seven.png  - a tightly cropped picture of Calculator's "7" button.

Create it in ONE of two ways:
  A) Automatic:  cd examples
                 python 06_image_based_click.py --capture
  B) Manual:     open Calculator, press Win+Shift+S, snip only the "7" button,
                 save it here as calc_seven.png

Re-capture the image whenever the theme (light/dark), display scaling
(100/125/150 %) or Calculator window size changes - image matching is
pixel based and will fail otherwise.
