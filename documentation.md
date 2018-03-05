# Documentation

### Overview
This application helps you calculate test-driven-development (TDD) violations over a certain time period in a Ruby on Rails project.


### Limitations
Currently, the code is hard-coded so that you are only checking for the last 65 days and only operates on your master branch. Both of these are in line to be opened up in the future.

### Setup
You will need to have a directory in your root directory called "repos". Inside of this directory, you can then create a folder (referred to later as the "outer folder") for each repository you want to track and then clone your git repo inside a folder within the outer folder (this new folder holding the git repo of your code will now be referred to as the "inner folder"). You must then set up the inner folder such that it is able to run cucumber and rspec testing without errors. You must use rbenv in order to change the ruby version for your repository environment.
Next you will need to make a few changes to your code such that you add cucumber and rspec to your default Rake task (https://stackoverflow.com/questions/16602446/how-to-add-a-rake-task-to-the-default-rake-task). You will also need to add a multi-formatter for SimpleCov (https://github.com/colszowka/simplecov#using-multiple-formatters). You will need to keep the default "SimpleCov::Formatter::HTMLFormatter" but will also need to add the SimpleCov-Cobertura XML formatter (https://github.com/dashingrocket/simplecov-cobertura) using "SimpleCov::Formatter::CoberturaFormatter".

### Methods Documentation
##### `check_tdd_commits`
Behavior: Checks if your request if "preemptive" or not and runs the TDD Checker on the commits specified
Args:
    `preemptive` (bool): Whether or not your request is preemptive or not
    `repo` (str): The full name (<username>/<reponame>) of your repository
    `branch` (str): If your request is not preemptive, then what branch you want to check
Returns:
    `ret` (str): JSON string with all of the XML test coverages for all commits checked
Errors:
    `err` (int): Possible error codes of -1, -2, -3. All signify a place in the code where something has gone wrong.

##### `compute_metric`
Behavior: Computes the metric based off the XML files that were already computed using check_tdd_commits. Uses `return_tdd_metric` to return the final metric.
Args:
    `repo` (str): The full name (<username>/<reponame>) of your repository
Returns:
    `ret` (str): JSON string with all metrics or error JSON string.

##### `return_tdd_metric`
Behavior: Returns the cached version of the metrics from file.
Args:
    `repo` (str): The full name (<username>/<reponame>) of your repository
Returns:
    `ret` (str): JSON string with all metrics or error JSON string.
