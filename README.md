# np-exploration-python
Template VSCode development container for local Data Science exploratory work

## Getting started

1. Create a git repository from the template [instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
2. Clone the new repository to your local computer [instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
3. Set the local environment variable `NIB_USERNAME` to your nib email (instructions below)
4. Login to the Docker registry on the Red Queen Platform (instructions below)
5. Open the project folder in VSCode (this will take a minute or two the first time while it does some setup steps such as building the container and setting your username for the Snowflake connector)
6. create file with the extension .ipynb to start an IPython notebook. At the top right, select np-exploration-python-PSNYYbGO-py3.9 as the kernel.

Example notebooks can be found in the `notebooks/examples` folder.

If you haven't used Jupyter notebooks in VSCode before, [this tutorial](https://code.visualstudio.com/docs/datascience/data-science-tutorial) may be helpful.

## Logging in to the Docker registry

Authenticate with AWS CONTROL GENERAL 

```
rqp auth --stage control --zone general --email <YOUR_EMAIL> --role readonly
```

Login to the Docker registry

```
rqp docker login
```


## Setting NIB_USERNAME

### Mac 

Assuming zshell is your default shell, add this line to .zprofile, subtitiuting your account name
```bash
export NIB_USERNAME=[your account name]@nib.com.au
```

### Windows

Open `System Properties` go to the `Advanced` tab. Click on `Environment Variables` and add `NIB_USERNAME` to the user variables with your nib email address as the value.


## Managing packages in the project

For convinience, some data science packages have been included in the base Docker image. However if you require [more](https://builtin.com/data-science/python-libraries-data-science) [packages](https://www.kaggle.com/code/parulpandey/useful-python-libraries-for-data-science), it is important to add them in a way that maintatins the reproducability of the project environment. The following steps will add a package dependency to the pyproject.toml file so that it will be automatically installed when a container is created from the project repository (e.g. when someone else clones the repo).

In the terminal, activate the virtual environment with:

```
source /root/.cache/pypoetry/virtualenvs/np-exploration-python-PSNYYbGO-py3.9/bin/activate
```

Add the package to the poetry manifest and install it to the virtual environment with:

```
poetry add [package name] --group project
```

You can remove a package by activating the virtual environment as above, then executing:

```
poetry remove [package name] --group project
```