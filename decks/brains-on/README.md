# Brains On

Built from the uploaded PPTX (`source/Brains_On-original.pptx`) in two passes:

    python3 fix.py   source/Brains_On-original.pptx step1.pptx icons
    python3 edit2.py step1.pptx brains-on.pptx icons logos

- `fix.py`: aesthetic pass (one dark ground, two greys per ground, RTL, pills, line icons, balance).
- `edit2.py`: round 2 (drop old slides 16/19/33, logo scatter on "which AI tools", thank-you slide before sources, renumber).
- PDF rendered with LibreOffice (fonts: Heebo, Karantina, Anton).
