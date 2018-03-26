import os
import re
import yaml
import xml.etree.ElementTree as ET
import subprocess
import sys


def check_commits(repo, commits):
    matchObj = re.match(r'.*\/(.*)', repo)
    short_name = matchObj.group(1)
    os.chdir(os.path.expanduser("~/repos"))
    if (not os.path.isdir("./{0}".format(short_name))):
        os.system("mkdir {0}".format(short_name))
    os.chdir("./{0}".format(short_name))
    calculate = []
    already_have = {}
    #print(os.getcwd())
    for commit in commits:
        if (not os.path.exists("commits/{0}.xml".format(commit))):
            calculate.append(commit)
        else:
            tree = ET.parse("commits/{0}.xml".format(commit))
            root = tree.getroot()
            already_have[commit] = ET.tostring(root).decode("utf-8")
    if calculate:
        os.chdir("./{0}".format(short_name))
        retVal = calculate_commits(repo, calculate)
        if retVal == -1 or retVal == -2:
            return retVal
        #change
        for i in already_have:
            retVal[i] = already_have[i]
        return retVal
    else:
        #change
        return already_have

def calculate_commits(repo, commits):
    # print(repo)
    # print(commits)
    try:
        os.system("git fetch --all")
        os.system("git reset --hard origin/master")
        travis_config=yaml.load(open('.travis.yml'))
        rvm_version = travis_config["rvm"][0]
        # print(rvm_version)
        # print(os.system("rbenv version"))
        # print(os.getcwd())
        os.system("rbenv local {0}".format(rvm_version))
        # print(os.system("rbenv version"))
    except:
        return -2

    try:    
        os.system("gem install bundler > /dev/null")
        os.system("bundle install > /dev/null")
        os.system("RAILS_ENV=test rake db:migrate > /dev/null")
        os.system("rake db:test:prepare > /dev/null")
    except:
        return -3
    
    retVal = {}
    for rollback in commits:
        os.system("git reset --hard {0}".format(rollback))
        os.system("bundle exec rake > /dev/null 2>&1")
        tree = ET.parse("coverage/coverage.xml")
        root = tree.getroot()
        retVal[rollback] = ET.tostring(root).decode("utf-8")
    save_to_file(retVal)
    return retVal

def save_to_file(commits_dict):
    os.chdir("..")
    if (not os.path.isdir("./commits")):
        os.system("mkdir commits")
    for commit in commits_dict:
        with open("commits/" + commit + ".xml", 'w') as file:
            file.write(commits_dict[commit])


def premptive_calculations(repo):
    matchObj = re.match(r'.*\/(.*)', repo)
    short_name = matchObj.group(1)
    os.chdir(os.path.expanduser("~/repos"))
    os.chdir("./{0}/{1}".format(short_name, short_name))
    try:
        os.system("git fetch --all")
        os.system("git reset --hard origin/master")
        #should be --since 1.days
        os.system("git log --pretty=format:'%H' --since=99.days > updated.txt")
    except:
        return -1
    commits = []
    with open("updated.txt", "r") as f:
        for line in f:
            commits.append(line[:-1])
    os.chdir("..")
    return check_commits(repo, commits)




#check_commits("saasbook/CS169_Great_Course_Guide", ["24fbadaa93833941b80c0db0d7fac8d2d4b8d5bd", "cd67b0a58c4ba757cb4bdf044329addf4291355a"])
premptive_calculations("saasbook/CS169_Great_Course_Guide")

# if __name__ == '__main__':
#     if sys.argv[1] == "preemptive":
#         if len(sys.argv) != 3:
#             raise ValueError("Not the right amount of arguments - preemptive")
#         print(premptive_calculations(sys.argv[2]))
#     else:
#         raise ValueError("Other operations not supported yet")