from core.Config import conf
import os
import matplotlib.pyplot as plt
import numpy as np

root = conf.resultsRoot
cResults = os.path.join(root, "NopolCResults.txt")
pResults = os.path.join(root, "NopolPCResults.txt")
condFile = open(cResults, "w+")
preconFile = open(pResults, "w+")
cell = []
total_time_count = 0
cond_time_count = 0
pre_time_count = 0
c_counts = []
p_counts = []
labels = []
# iterate over all projects (= Chart, Lang, Math, Time)
for project in os.listdir(root):
    if project.__contains__("Math") or project.__contains__("Lang") or project.__contains__(
            "Chart") or project.__contains__("Time"):
        condFile.write("Project: " + project + "\n")
        preconFile.write("Project: " + project + "\n")
        bugs = []
        c_count = 0
        p_count = 0
        projectroot = os.path.join(root, project)
        bugId = 1
        # sort the bugs in ascending order
        for _ in os.listdir(projectroot):
            bugs.append(bugId)
            bugId += 1
        bugs.sort()
        # filter out relevant results for each bug and each repair strategy
        for bugId in bugs:
            cond_time = 0
            pre_time = 0
            bugPath = os.path.join(projectroot, str(bugId))
            condPath = os.path.join(bugPath, "NopolC")
            preconPath = os.path.join(bugPath, "NopolPC")
            con_fix = False
            pre_fix = False

            # check conditional strategy
            if os.listdir(condPath).__contains__("results.txt"):
                resultsFileC = condPath + "/results.txt"
                results = open(resultsFileC, "r")
                if results.read().__contains__("----PATCH FOUND----"):
                    c_count += 1
                    con_fix = True
                    results.close()
                    results = open(resultsFileC, "r")
                    for line in results:
                        if "Execution time" in line:
                            cond_time = round(int(line[23:-3]) / 1000)
                            cond_time_count += cond_time
                    results.close()
                    condFile.write("bug: " + str(bugId) + " patch: yes " + "time " + str(cond_time) + "s\n")
                else:
                    condFile.write("bug: " + str(bugId) + " patch: no " + "\n")
            else:
                condFile.write("bug: " + str(bugId) + " patch: no " + "\n")

            # check missing precondition strategy
            if os.listdir(preconPath).__contains__("results.txt"):
                resultsFilePC = preconPath + "/results.txt"
                results = open(resultsFilePC, "r")
                if results.read().__contains__("----PATCH FOUND----"):
                    p_count += 1
                    pre_fix = True
                    results.close()
                    results = open(resultsFilePC, "r")
                    for line in results:
                        if "Execution time" in line:
                            pre_time = round(int(line[23:-3]) / 1000)
                            pre_time_count += pre_time
                    results.close()
                    preconFile.write("bug: " + str(bugId) + " patch: yes " + "time " + str(pre_time) + "s\n")
                    if not con_fix:
                        total_time_count += pre_time
                        cell.extend([[project[0].upper() + str(bugId), "PC", str(pre_time) + "s"]])
                else:
                    condFile.write("bug: " + str(bugId) + " patch: no " + "\n")
            else:
                if con_fix:
                    total_time_count += cond_time
                    cell.extend([[project[0].upper() + str(bugId), "C", str(cond_time) + "s"]])
                preconFile.write("bug: " + str(bugId) + " patch: no " + "\n")

            if con_fix and pre_fix:
                cell.extend([[project[0].upper() + str(bugId), "C&PC",
                              "C: " + str(cond_time) + "s / PC: " + str(pre_time) + "s"]])
                if cond_time < pre_time:
                    total_time_count += cond_time
                else:
                    total_time_count += pre_time

        c_counts.append(c_count)
        p_counts.append(p_count)
        condFile.write("-----------------------------------\n")
        preconFile.write("-----------------------------------\n")

condFile.close()
preconFile.close()

cond_count = 0
pre_count = 0
for item in cell:
    if item.__contains__("C") or item.__contains__("C&PC"):
        cond_count += 1
    if item.__contains__("PC") or item.__contains__("C&PC"):
        pre_count += 1
patch_count = len(cell)
c_counts.append(cond_count)
p_counts.append(pre_count)
cond_time_avg = round(cond_time_count / cond_count)
pre_time_avg = round(pre_time_count / pre_count)
time_avg = round(total_time_count / patch_count)
cell.extend([[str(patch_count) + " patches found for 224 bugs", str(cond_count) + " C & " + str(pre_count) + " PC",
              "Average time:   P&C: " + str(time_avg) + "s / C: " + str(cond_time_avg) + "s / PC: " + str(
                  pre_time_avg) + "s"]])

colors = [['w', 'w', 'w']] * (len(cell) - 1)
colors.append(['silver', 'silver', 'silver'])

# plot table of fixed bugs in total
columns = ('BugId', 'Repair Mode', 'Time in s')
fig, ax = plt.subplots()
# hide axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

ax.table(cellText=cell, colLabels=columns, colColours=['silver', 'silver', 'silver'], loc='center', cellColours=colors)

fig.tight_layout()
plt.savefig(os.path.join(root, "ResultsTable.eps"), format='eps')
plt.clf()

# plot table of strategy comparison
labels = ['Chart', 'Math', 'Time', 'Lang', 'Total']

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, c_counts, width, label='Conditional')
rects2 = ax.bar(x + width / 2, p_counts, width, label='Precondition')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Found patches')
ax.set_title('Comparison of the conditional & missing precondition strategy')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.savefig(os.path.join(root, "StrategyComparison.eps"), format='eps')
