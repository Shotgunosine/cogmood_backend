.. image:: https://img.shields.io/badge/python-3.6+-blue.svg
        :target: https://www.python.org/downloads/release/python-360/

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
        :target: https://github.com/nivlab/NivLink/blob/master/LICENSE
        
.. image:: https://zenodo.org/badge/182183266.svg
   :target: https://zenodo.org/badge/latestdoi/182183266

NivTurk
=======

Niv lab tools for securely serving and storing data from online computational psychiatry experiments.
Adapted by the NIMH MLC for the CogMood experiments.

Documentation
^^^^^^^^^^^^^

Assigning a sequential ID to each participant depends on the postgres docker container. Obtainable via:

```
docker pull postgres
```

Create an environemntal variable DBPW set to the password you'd like for your database, then start the container from the app directory with the following command:

```
docker run --name cmbedb -v $PWD/data/database:/var/lib/postgresql/data -e POSTGRES_PASSWORD=$DBPW --shm-size=256MB  -p 5432:5432 -d postgres
```

Note that this exposes your postgres port on the machine you're running on, which is somewhat insecure.

For details on how to serve your experiment, how the code is organized, and how data is stored, please see the
`Documentation <https://nivlab.github.io/nivturk>`_.

Citation
^^^^^^^^

If you use this library in academic work, please cite the following:

  | Samuel Zorowitz & Daniel Bennett. (2022). NivTurk (v1.2-prolific). Zenodo. https://doi.org/10.5281/zenodo.6609218

Acknowledgements
^^^^^^^^^^^^^^^^
NivTurk was developed with support from the National Center for Advancing Translational Sciences (NCATS), a component of the National Institute of Health (NIH), under award number UL1TR003017.
