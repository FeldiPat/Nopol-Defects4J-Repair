import os
from os.path import expanduser

class Config(object):
    """Runner configurations"""

    def __init__(self):
        defects4jRepairRoot = os.path.join(os.path.dirname(__file__), '../../../')
        self.defects4jRepairRoot = defects4jRepairRoot
        self.projectsRoot = os.path.join(defects4jRepairRoot, "libs/projects")
        self.defects4jRoot = expanduser("~/Documents/Uni/Semester2/Seminar_APR/experiments.nosync/defects4j")
        self.resultsRoot = os.path.join(defects4jRepairRoot, "results/2020-march")
        self.z3Root = os.path.join(defects4jRepairRoot, "libs/z3_for_mac")
        self.javaHome = expanduser("~/../../Library/Java/JavaVirtualMachines/jdk1.8.0_231.jdk/Contents/Home/bin/")
        self.javaHome8 = expanduser("~/../../Library/Java/JavaVirtualMachines/jdk1.8.0_231.jdk/Contents/Home/")
        self.javaArgs = "-Xmx2560m"


conf = Config()
