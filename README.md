# Crazy Matrix
Allows the creation of visualization using combined mathematical expressions using each pixels coordinates as arguments.

## Install
### Create a conda environment
```bash
conda init bash # => Open new terminal
conda create --name crazy_matrix python=3.7
conda install --name crazy_matrix numpy
conda install --name crazy_matrix uuid
conda install --name crazy_matrix tk
conda install --name crazy_matrix matplotlib #xxx entfernen?
conda install --name crazy_matrix PyYAML
conda install --name crazy_matrix -c conda-forge pykwalify
```

### Activate the conda environment and start the program
```bash
cd crazy_matrix/
conda activate crazy_matrix
python main.py
```

## Here are some screenshots on what is possible:
![border](images/border.png "border")

![gradient](images/gradient.png "gradient")

![cart2pol](images/cart2pol.png "cart2pol")

![modulo](images/modulo.png "modulo")

![sphere](images/sphere.png "sphere")

![normal_distribution](images/normal_distribution.png "normal_distribution")

![gravitation](images/gravitation.png "gravitation")

![oscillating](images/oscillating.png "oscillating")

![sin_rad](images/sin_rad.png "sin_rad")

![mandelbrot](images/mandelbrot.png "mandelbrot")


### Naming convention of file extensions
* cmc = crazy matrix circuit
* cmb = crazy matrix black (box)
* cmr = crazy matrix repeat (box)