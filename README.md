[![image](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/nivlab/NivLink/blob/master/LICENSE)

[![image](https://zenodo.org/badge/182183266.svg)](https://zenodo.org/badge/latestdoi/182183266)

# Cogmood Backend

Backend for the NIMH MLC's CogMood experiments, adapted from the Niv
lab tools for securely serving and storing data from online
computational psychiatry experiments.

# Documentation

For details on how to serve your experiment, how the code is organized,
and how data is stored, please see the
[Documentation](https://nivlab.github.io/nivturk).

## Running in docker for testing
1. cd to the cogmood_backend directory
2. Build the docker file:  
    `docker build -t cogmood_backend .`
3. Run with directories bound:  
    `docker run --name running_backend -dp 5000:5000 -v $PWD/data:/cogmood_backend/data -v $PWD/metadata:/cogmood_backend/metadata cogmood_backend`
4. Run tests:  
    `docker exec running_backend pytest`  

You can visit the site at 127.0.0.1:5000?PROLIFIC_PID=[some unused number]. 
If you install all the requirements in a conda environment or some such, 
you can also run pytest outside of docker.

# Citation

If you use this library in academic work, please cite the following:

> | Samuel Zorowitz & Daniel Bennett. (2022). NivTurk (v1.2-prolific).
>   Zenodo. <https://doi.org/10.5281/zenodo.6609218>

# Acknowledgements

NivTurk was developed with support from the National Center for
Advancing Translational Sciences (NCATS), a component of the National
Institute of Health (NIH), under award number UL1TR003017.
