#!/usr/bin/env python

import argparse
from core.projects.LangProject import LangProject
from core.projects.MathProject import MathProject
from core.projects.ChartProject import ChartProject
from core.projects.TimeProject import TimeProject

from core.tools.Ranking import Ranking
from core.tools.NopolPC import NopolPC
from core.tools.NopolC import NopolC


def initParser():
    parser = argparse.ArgumentParser(description='Run Nopol on defects4j dataset')
    parser.add_argument('-project', required=True, help='Which project (math, lang, time, all)')
    parser.add_argument('-mode', required=True, help='Which repair mode (ranking, conditional, precondition')
    parser.add_argument('-id', help='Bug id, all')
    return parser.parse_args()


args = initParser()
project = None
tool = None
projects = None
if args.project == "Lang":
    projects = [LangProject()]
elif args.project == "Math":
    projects = [MathProject()]
elif args.project == "Chart":
    projects = [ChartProject()]
elif args.project == "Time":
    projects = [TimeProject()]
elif args.project == "all":
    projects = [ChartProject(), LangProject(), MathProject(), TimeProject()]


if args.mode == "NopolPC":
    tool = NopolPC()
elif args.mode == "NopolC":
    tool = NopolC()
elif args.mode == "Ranking":
    tool = Ranking()

bugCount = None
if args.id == "all":
    for project in projects:
        if project.__module__.__contains__("Lang"):
            bugCount = 65
        elif project.__module__.__contains__("Math"):
            bugCount = 106
        elif project.__module__.__contains__("Chart"):
            bugCount = 26
        elif project.__module__.__contains__("Time"):
            bugCount = 27
        for bugId in range(bugCount):
            tool.run(project, bugId+1)

else:
    for project in projects:
        bugId = int(args.id)
        tool.run(project, bugId)
