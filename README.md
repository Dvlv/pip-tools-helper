# pip-tools-helper
Interface for pip-tools

## Installing

Mark it as executable and put it somewhere in your PATH

```bash
chmod +x pth.py
ln -s pth.py ~/bin/pth
```

## Usage

### Beforehand
Create and source a virtual environment as you normally would, then add a `requirements` folder.

```bash
mkdir MyProject
cd MyProject
python3 -m venv env
source env/bin/activate
mkdir requirements
```

### Installing packages
To install a package to your global `requirements.txt` file, just run `pth install <packages>`.

```bash
pth install flask

pth install flask peewee ansible
```

To install development or CI dependencies, use the `-e` flag or `--env`, followed by the environment name.

```bash
pth -e dev install pylint

pth -e dev -e ci install pytest
```

`dev` and `ci` are not particular, you can specify any arbitrary set of requirements under any name.

### Removing packages
To remove, use `remove` or `uninstall`.

```bash
pth remove flask

pth uninstall peewee
```

If the package is in a named set of requirements, again use `-e` or `--env` to specify.

```bash
pth -e dev remove pytest
```

### Compiling / Syncing
If your `.in` files are already created, there is no need to use `install`. Just compile then sync.

```bash
cp OtherProject/requirements/requirements.in requirements/requirements.in
pth compile
pth sync
```

### Syncing without dev
By default, if you have `requirements-dev.txt` and you run `pth sync` it will sync the development requirements.
If you don't want this, pass `--no-dev`

```bash
pth sync --no-dev
```

### Install without syncing
If you want to add a package to a `.in` file without syncing, pass `--no-sync`

```bash
pth install --no-sync flask
```
