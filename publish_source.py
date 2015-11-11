import application
from upload2google import upload2google
import platform
import sys
sys.path.append('src')
sys.path.append('.')
import utils

file_path = "dist/{0}-{1}-src.{2}" \
    .format(application.NAME, application.VERSION, "tar.gz")
project = "almoviesrenamer"
summary = application.NAME + " " + application.VERSION + " Source"
labels = ["Featured", "Type-Source", "OpSys-All"]

upload2google(file_path, project, summary, labels)
