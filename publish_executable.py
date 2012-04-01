
from upload2google import upload2google
import platform
import sys
sys.path.append('src')
sys.path.append('.')
import utils

if platform.system() == "Windows":
    extension = "zip"
else:
    extension = "tar.gz"
file_path = "dist/{0}-{1}-{2}.{3}" \
    .format(utils.PROGRAM_NAME, utils.PROGRAM_VERSION, platform.system(), extension)
project = "almoviesrenamer"
summary = utils.PROGRAM_NAME + " " + utils.PROGRAM_VERSION + " " + platform.system()
labels = ["Featured", "Type-Archive"]
if platform.system() == "Windows":
    labels.append("OpSys-Windows")
else:
    labels.append("OpSys-Linux")

upload2google(file_path, project, summary, labels)

