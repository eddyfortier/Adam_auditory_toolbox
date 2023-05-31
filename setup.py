from setuptools import find_packages, setup

setup(name="Adam_auditory_toolbox",
      version="0.0.1",
      description="Description is unavailable at the moment.",
      license="Creative Commons Attribution Share Alike 4.0 International",
      author="E. Fortier",
      author_email="eddy.fortier@umontreal.ca",
      url="https://github.com/eddyfortier/Adam_auditory_toolbox",
      install_requires=["numpy", "pandas",
                        "plotly", "matplotlib",
                        "sklearn", "colorama",
                        "seaborn", "notebook",
                       ],
      packages=find_packages())
