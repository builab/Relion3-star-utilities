# Relion3-star-utilities
A collection of star file utilities for Relion 3.0


# relion3_add_beamtiltclass.py
Convert the beam tilt file name pattern to beam tilt class for Polishing

McGill Krios beam tilt pattern

  xxx_micrographNo_HoleId-ShotID.tif
 
  E.g. Micro_00000_1-1.tif, Micro_00003_1-3.tif, Micro_00010_3-2.tif

$python relion3_micrograph_add_beamtiltclass.py --istar micrographs_ctf.star --ostar micrographs_ctf_beamtiltclass.star --holeno 4

# relion3_1_add_opticgroups.py
Similar to relion3_add_beamtiltclass.py but now is used for relion 3.1 to accomodate data_optics table.
It is tailored to McGill Krios FEMR beam tilt pattern above
The script replicates optic groups in data_optic table (indicate by --nogroup) and replaces rlnOpticsGroup in data_particles table with a group number from the micrograph name. Different to the script above, this script using pattern to identify group so it is a bit more robust (McGill pattern _(\d+-\d+).mrc is used as default). It can be best used for micrographs after MotionCorrection or CtfFind. It can also be used for particle file.

$python relion3_1_add_opticgroups.py --istar micrographs_ctf.star --ostar micrographs_ctf_opticgroups.star --nogroup 16

Using a different pattern (Python regex format)
$python relion3_1_add_opticgroups.py --istar micrographs_ctf.star --ostar micrographs_ctf_opticgroups.star --nogroup 16 --pattern "_(\d+-\d+).mrc"


# plot_beamtilt_class.py
Plot the beam tilt estimation from CtfRefine

$python plot_beamtilt_class.py beamtilt_iter-fit_class_*.txt

Output: beamtilt_class.png

# relion3_0_filter_short_microtubules.py
Filtering out microtubules with less particles than a threshold

$relion3_0_filter_short_microtubules.py --istar particles.star --ostar particles_filtered.star --minpart 10


# relion3_0_plot_microtubule_alignment.py
Ploting out Phi, Psi, Theta & Shifts for visualization of accurate alignment

$relion3_0_plot_microtubule_alignment.py --istar particles.star --im fit --minpart 10

--im directory to output the graphic

Output: angle plot for each microtubule


