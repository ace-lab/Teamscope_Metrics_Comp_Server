# Documentation

### Overview
This application helps you calculate test-driven-development (TDD) violations over a certain time period in a Ruby on Rails project.


### Limitations
Currently, the code is hard-coded so that you are only checking for the last 65 days and only operates on your master branch. Both of these are in line to be opened up in the future.

### Setup
You will need to have a directory in your root directory called "repos". Inside of this directory, you can then create a folder (referred to later as the "outer folder") for each repository you want to track and then clone your git repo inside a folder within the outer folder (this new folder holding the git repo of your code will now be referred to as the "inner folder"). You must then set up the inner folder such that it is able to run cucumber and rspec testing without errors. You must use rbenv in order to change the ruby version for your repository environment.
Next you will need to make a few changes to your code such that you add cucumber and rspec to your default Rake task (https://stackoverflow.com/questions/16602446/how-to-add-a-rake-task-to-the-default-rake-task). You will also need to add a multi-formatter for SimpleCov (https://github.com/colszowka/simplecov#using-multiple-formatters). You will need to keep the default "SimpleCov::Formatter::HTMLFormatter" but will also need to add the SimpleCov-Cobertura XML formatter (https://github.com/dashingrocket/simplecov-cobertura) using "SimpleCov::Formatter::CoberturaFormatter".

### How to run the metrics once the project directory is set up
##### GitHub Metrics
Call the  `github_comp_metric.py` file with the long-name of the repo you want to run this metric on as a command-line argument. 

Ex. `python github_comp_metric.py <insert repo long-name here>`.

##### Travis CI Metrics
Add a line of code at the bottom of the `travis_comp_metric.py` file, calling on the `get_all_travis_data` method with the long-name of the repo as an argument to the function.

Ex. `get_all_travis_data("<insert repo long-name here>")`

##### CodeClimate Metrics
Add a line of code at the bottom of the `codeclimate_comp_metric.py` file, calling on the `get_all_codeclimate_data` method with the long-name of the repo as an argument to the function.

Ex. `get_all_codeclimate_data("<insert repo long-name here>")`

##### Computational Metric
Call the  `tddchecker_comp.py` file with the long-name of the repo you want to run this metric on as a command-line argument. 

Ex. `python tddchecker_comp.py <insert repo long-name here>`.

##### TDD Metric
Call the  `metric_tddchecker.py` file with the long-name of the repo you want to run this metric on as a command-line argument. 

NOTE: In order to do this, you must have already computed each commit that you want to get this metric for as per the [Computational Metric](#computational-metric). 

Ex. `python metric_tddchecker.py <insert repo long-name here>`.


### Methods Documentation - DEPRECATED
##### `check_tdd_commits`
Behavior: Checks if your request if "preemptive" or not and runs the TDD Checker on the commits specified  
Args:  
&nbsp;&nbsp;&nbsp;&nbsp;`preemptive` (bool): Whether or not your request is preemptive or not  
&nbsp;&nbsp;&nbsp;&nbsp;`repo` (str): The full name (<username>/<reponame>) of your repository  
&nbsp;&nbsp;&nbsp;&nbsp;`branch` (str): If your request is not preemptive, then what branch you want to check  
Returns:  
&nbsp;&nbsp;&nbsp;&nbsp;`ret` (str): JSON string with all of the XML test coverages for all commits checked  
Errors:  
&nbsp;&nbsp;&nbsp;&nbsp;`err` (int): Possible error codes of -1, -2, -3. All signify a place in the code where something has gone wrong.

##### `compute_metric`
Behavior: Computes the metric based off the XML files that were already computed using check_tdd_commits. Uses `return_tdd_metric` to return the final metric.  
Args:  
&nbsp;&nbsp;&nbsp;&nbsp;`repo` (str): The full name (<username>/<reponame>) of your repository  
Returns:  
&nbsp;&nbsp;&nbsp;&nbsp;`ret` (str): JSON string with all metrics or error JSON string.

##### `return_tdd_metric`
Behavior: Returns the cached version of the metrics from file.  
Args:  
&nbsp;&nbsp;&nbsp;&nbsp;`repo` (str): The full name (<username>/<reponame>) of your repository  
Returns:  
&nbsp;&nbsp;&nbsp;&nbsp;`ret` (str): JSON string with all metrics or error JSON string.
