import os
import subprocess
from threading import Timer

from core.Tool import Tool
from core.Config import conf


class Nopol(Tool):
    """docstring for Nopol"""

    def __init__(self, name="Nopol"):
        super(Nopol, self).__init__(name, "nopol")

    def run(self, project, id):
        log = self.runNopol(project, id)
        result = log.split('----INFORMATION----')
        if len(result) > 1:
            print (result[1])
            self.parseLog(result[1], project, id)

    def runNopol(self, project, id, mode, type, synthesis, oracle):
        workdir = self.initTask(project, id)
        classpath = ""
        for index, cp in project.classpath.items():
            if id <= int(index):
                for c in cp.split(":"):
                    if classpath != "":
                        classpath += ":"
                    classpath += os.path.join(workdir, c)
                break
        source = ""
        for index, src in project.src.items():
            if id <= int(index):
                source = os.path.join(workdir, src['srcjava'])
                break
        for lib in project.libs:
            if os.path.exists(os.path.join(workdir, "lib", lib)):
                classpath += ":" + os.path.join(workdir, "lib", lib)
        classpath += ":" + self.jar

        cmd = 'cd ' + workdir + ';'
        cmd += 'time java %s -cp %s:%s/../lib/tools.jar %s' % (conf.javaArgs, self.jar, conf.javaHome, self.main)
        cmd += ' --mode ' + mode
        if self.name != "Nopol":
            cmd += ' --type ' + type
        cmd += ' --oracle ' + oracle
        cmd += ' --synthesis ' + synthesis
        cmd += ' --solver-path ' + conf.z3Root
        cmd += ' --source ' + source
        cmd += ' --classpath ' + classpath + ';'

        logPath = os.path.join(project.logPath, str(id), self.name, "stdout.log.full")
        if not os.path.exists(os.path.dirname(logPath)):
            os.makedirs(os.path.dirname(logPath))
        log = open(logPath, 'w')
        p = subprocess.Popen(cmd, shell=True, stdout=log)
        timeout = 600  # 10min timeout
        timer = Timer(timeout, p.kill)
        try:
            timer.start()
            p.communicate()
        finally:
            timer.cancel()

        # kill the running processes if timeout occurs
        jpsOut = subprocess.check_output("jps -l", shell=True)
        for line in jpsOut.splitlines():
            if 'fr.inria.lille.repair.Main' in str(line):
                tokens = line.split(' ')
                subprocess.call('kill ' + tokens[0], shell=True)
            elif 'com.gzoltar.core.instr.Runner' in str(line):
                tokens = line.split(' ')
                subprocess.call('kill ' + tokens[0], shell=True)

        with open(logPath) as data_file:
            return data_file.read()

    def parseLog(self, log, project, id):
        path = os.path.join(project.logPath, str(id), self.name, "results.txt")
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        file = open(path, "w")
        file.write(log)
        file.close()
