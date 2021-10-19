# BI_2021_Python
Collection of tasks and projects made at [Bioinformatics institute](https://bioinf.me/en) 

### nucleic_acids_utility.py
Utility for manipulation with nucleic acid sequences (DNA or RNA). The utility reads a command and a sequence of nucleic acid from the user, then print a result. It saves the case of letters (e.g complement AtGc - TaCg).

Available commands:

- **exit** — complete programm execution 
- **transcribe** — print transcribed sequence (can be implemented only to RNA)
- **reverse** — print inverted sequence 
- **complement** — print complementary sequence
- **reverse complement** — print inverted complementary sequence 

### units_converter.py
Program for temperature convertation into different units.

Available T units: celsius (C), kelvin (K), fahrenheit (F). 

Formulas for convertation: 
- from **C** to **K**: T + 273.15
- from **C** to **F**: 1.8 * T + 32
- from **K** to **C**: T - 273.15
- from **K** to **F**: 1.8 * (T-273.15) + 32
- from **F** to **C**: 5/9 * (T-32)
- from **F** to **K**: 5/9 * (T-32) + 273.15
