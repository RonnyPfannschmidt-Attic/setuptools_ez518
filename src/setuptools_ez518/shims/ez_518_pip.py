import os
import sys
import subprocess
import logging
log = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(name)s [%(levelname)s] %(message)s"))
log.addHandler(handler)

DISABLED = os.environ.get('SETUPTOOLS_EZ518') == 'disabled'
DEBUG = os.environ.get('SETUPTOOLS_EZ518') == 'debug'
log.setLevel(logging.DEBUG if DEBUG else logging.INFO)
PACKAGGE_INTO = os.environ.get(
    'SETUPTOOLS_EZ518_PACKAGGE_INTO', '.cache/python-ez518')


def normalize_to_folder(path):
    path = os.path.normpath(os.path.abspath(path))
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    return path


def setup(path='.', packages_into='.cache/python-ez518', disabled=DISABLED):
    if disabled:
        log.warn("disabled, not downloading anything")
    else:
        log.info('to disable set SETUPTOOLS_EZ518=disabled in the environment')
    path = normalize_to_folder(path)
    tomlpath = os.path.join(path, 'pyproject.toml')
    if not os.path.isfile(tomlpath):
        log.error("%r missing, not doing anything", tomlpath)
        return

    target_folder = os.path.join(path, packages_into)
    log.info('install target: %s', target_folder)
    sys.path.insert(0, target_folder)

    log.info("installing toml")
    subprocess.check_call([
        sys.executable, '-m',
        'pip', 'install', '-q',
        '-t', target_folder,
        "toml",
    ])

    import toml
    with open(os.path.join(path, 'pyproject.toml')) as fp:
        data = toml.load(fp)
    log.debug('toml data: %r', data)
    requires = data.get('build-system', {}).get('requires', [])
    log.debug('build requirements %r', requires)
    subprocess.check_call([
        sys.executable, '-m',
        'pip', 'install', '-U',
        '-t', target_folder,
        ] + requires)
