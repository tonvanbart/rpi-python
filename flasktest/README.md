Flask project with Raspberry Pi Sense Hat integration.
To use, clone the project on a Pi with a Sense Hat and the required package installed as per the documentation:

[https://sense-hat.readthedocs.io/en/latest/](https://sense-hat.readthedocs.io/en/latest/)

Then activate a venv, giving it access to site packages:

```
python3 -m venv --system-site-packages venv
```

Or if you already have a venv, check `venv/pyvenv.cfg`, it should contain the following line:

```
include-system-site-packages = true
```

Activate the venv `source venv/bin/activate` and install the other requirements:

```
pip install -r requirements.txt
```


    