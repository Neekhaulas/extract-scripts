import os
from pathlib import Path
from invoke import run as _run, task


def run(*args, **kwargs):
	kwargs.setdefault("echo", True)
	return _run(*args, **kwargs)


BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
BASE_DATA_DIR = Path("/mnt/home")
BUILD_DIR = BASE_DIR / "build"

# Base and output path for 'hsb' ngdp directory
NGDP_DIR = BASE_DATA_DIR / "ngdp"
NGDP_OUT = NGDP_DIR / "out"

# Directory storing the build data files
NGDP_DATA_DIR = BASE_DATA_DIR / "data/ngdp/hsb"

# External repositories used
REPOSITORIES = ("HearthstoneJSON", "Sunwell", "hs-fonts")


@task
def update_repositories(context):
	for name in REPOSITORIES:
		url = "git@github.com:HearthSim/{name}.git".format(name=name)
		repo = BASE_DIR / name

		if not repo.exists():
			run("git clone {url} {repo}".format(url=url, repo=repo))
		else:
			run("git -C {repo} pull".format(repo=repo))

	run("git -C {BASE_DIR} submodule init".format(BASE_DIR=BASE_DIR))
	run("git -C {BASE_DIR} submodule update".format(BASE_DIR=BASE_DIR))


@task
def prepare_patch_directories(context, build):
	HSBUILDDIR = BUILD_DIR / "extracted" / build
	HS_RAW_BUILDDIR = NGDP_DATA_DIR / build

	if HSBUILDDIR.exists():
		print("{HSBUILDDIR} already exists, not overwriting.".format(HSBUILDDIR=HSBUILDDIR))
	else:
		os.makedirs(HSBUILDDIR)

		if HS_RAW_BUILDDIR.exists():
			print("{HS_RAW_BUILDDIR} already exists, skipping download checks.".format(HS_RAW_BUILDDIR=HS_RAW_BUILDDIR))
		else:
			if not NGDP_OUT.exists():
				print("No {NGDP_OUT} directory. Run downloader in {NGDP_DIR}".format(
					NGDP_OUT=NGDP_OUT, NGDP_DIR=NGDP_DIR,
				))
				exit(2)

			run("mv {NGDP_OUT} {HS_RAW_BUILDDIR}".format(NGDP_OUT=NGDP_OUT, HS_RAW_BUILDDIR=HS_RAW_BUILDDIR))

		run("ln -sv {HS_RAW_BUILDDIR} {HSBUILDDIR}".format(HS_RAW_BUILDDIR=HS_RAW_BUILDDIR, HSBUILDDIR=HSBUILDDIR))
