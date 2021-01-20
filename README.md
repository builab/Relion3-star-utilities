# Relion3-star-utilities
A collection of star file utilities for Relion 3.0


# relion3_micrograph_add_beamtiltclass.py
Convert the beam tilt file name pattern to beam tilt class for Polishing

McGill Krios beam tilt pattern

  xxx_micrographNo_HoleId_ShotID.tif
 
  E.g. Micro_00000_1_1.tif, Micro_00003_1_3.tif, Micro_00010_3_2.tif

$python relion3_micrograph_add_beamtiltclass.py --istar micrographs_ctf.star --ostar micrographs_ctf_beamtiltclass.star --holeno 4

# plot_beamtilt_class.py
Plot the beam tilt estimation from CtfRefine

$python plot_beamtilt_class.py beamtilt_iter-fit_class_*.txt

Output: beamtilt_class.png

#relion3_0_filter_short_microtubules.py
Filtering out microtubules with less particles than a threshold

$relion3_0_filter_short_microtubules.py --istar particles.star --ostar particles_filtered.star --minpart 10



