# This sphinx extension downloads and installs lightningcss and then uses it to bundle our
# theme CSS files. We're using binaries built by lightningcss but they only distribute them
# through npm - so we have to deal with platform detection and then download the .tar from
# npm and extract it ourselves.
#
# @todo This could be extracted to a standalone sphinx extension and (I think) use PyPi to
#       mirror the npm lightningcss binaries as python platform-specific wheels.
from urllib.request import urlretrieve
from sphinx.util import logging
import platform
import os
import shutil
import subprocess
import tarfile
from tempfile import gettempdir

def detect_lightningcss_platform():
    os = platform.system()
    lib, _ =platform.libc_ver()
    arch = platform.machine()

    # @todo there are lightningcss binaries for many platforms, but the names don't map directly to
    #       the values python provides and it would need a bit of testing to be confident I was
    #       getting them correct for other environments. For now, just check it's the expected
    #       platform for our local Docker and for ReadTheDocs

    if os != 'Linux':
      raise Exception(f"Installation on '{os}' is not yet supported")

    if lib != 'glibc':
      raise Exception(f"Installation with '{lib}' c compiler is not yet supported")

    if arch != 'x86_64':
      raise Exception(f"Installation on '{arch}' architecture is not yet supported")

    return 'linux-x64-gnu'

def install_lightningcss(version):
    platform = detect_lightningcss_platform()

    # Place the binary in the working directory - it should survive across docker restarts when working locally
    filename = f"{os.getcwd()}/lightningcss-{platform}-{version}"
    if os.path.isfile(filename):
      return filename

    # Download from the nodejs release (these packages just contain a standalone binary for each platform)
    download_url = f"https://registry.npmjs.org/lightningcss-cli-linux-x64-gnu/-/lightningcss-cli-{platform}-{version}.tgz"

    logger = logging.getLogger(__name__)
    logger.info(f"Downloading lightningcss from {download_url}")
    lightning_tar , _ = urlretrieve(download_url)

    # Unpack the lightningcss binary from the archive to the tmpdir
    tmpdir = gettempdir()
    tar = tarfile.open(lightning_tar)
    tar.extract('package/lightningcss', path=tmpdir, filter='data')

    # Move the executable to the working dir
    shutil.move(f"{tmpdir}/package/lightningcss", filename)
    logger.info(f"Unpacked lightningcss to {filename}")

    return filename

def compile_css(app,exc):
    if app.builder.format != 'html':
      return
    if exc:
      # there was an exception
      return

    lightningcss_bin = install_lightningcss('1.29.3')
    logger = logging.getLogger(__name__)

    # Run it
    input_css = '_theme/css/behat-docs.css'
    output_css = app.outdir / '_static/css/behat-docs.css'
    logger.info(f"Compiling {input_css} to {output_css} with lightningcss")
    subprocess.run([
      lightningcss_bin,
      '--bundle',
      '--minify',
      '--targets',
      '>=0.25%',
      input_css,
      '-o',
      output_css
    ])

def setup(app):
    app.connect('build-finished', compile_css)
