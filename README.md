# todocli-python

Implementing project ideas from [here](https://github.com/dreamsofcode-io/goprojects/tree/main)

## Overview

This is a lightweight todo list app for the CLI using `python`, `click`, `sqlite3`, `SQLAlchemy` and `prettytable`.

Clone the repo and alias the tasks scripts as `tasks` to follow along.

```sh
alias tasks='python src/todocli_python/tasks.py'
```

### Add tasks

`In:`
```sh
tasks add "Follow the tasks tutorial"
tasks add "Finish adding at least two tasks"
```
### List tasks


`In:`
```sh
tasks list
```
`Out:`
```sh

Tasks @ 15:27 21-Sep-2024
+----+----------------------------------+-------------+
| ID | Description                      | Created     |
+----+----------------------------------+-------------+
| 1  | Follow the tasks tutorial        | 31 secs ago |
| 2  | Finish adding at least two tasks | 10 secs ago |
+----+----------------------------------+-------------+ 

```

Adding `-a` or `--all` will also display completed tasks.

### Complete a task


`In:`
```sh
tasks complete 1
tasks list
```
`Out:`
```sh


Tasks @ 15:29 21-Sep-2024
+----+----------------------------------+------------+
| ID | Description                      | Created    |
+----+----------------------------------+------------+
| 2  | Finish adding at least two tasks | 1 mins ago |
+----+----------------------------------+------------+ 

```

### Clear completed tasks

`In:`
```sh
tasks clear
```

Adding `-a` or `--all` will ***delete all tasks***.

### Delete tasks

To delete the task with ID=1:

`In:`
```sh
tasks delete 1
```

## Notable Packages Used

- `click` simple cli module
- `sqlalchemy` for handling db connections and models
- `sqlite3` Simple in memory db
- `prettytable` Easy way to display tabular data

# The inspiration

## Goal

Create an cli application for managing tasks in the terminal.

```
$ tasks
```

## Requirements

Should be able to perform crud operations via a cli on a data file of tasks. The operations should be as follows:

```
$ tasks add "My new task"
$ tasks list
$ tasks complete 
```

### Add

The add method should be used to create new tasks in the underlying data store. It should take a positional argument with the task description

```
$ tasks add <description>
```

for example:

```
$ tasks add "Tidy my desk"
```

should add a new task with the description of "Tidy my desk"

### List

This method should return a list of all of the **uncompleted** tasks, with the option to return all tasks regardless of whether or not they are completed.

for example:

```
$ tasks list
ID    Task                                                Created
1     Tidy up my desk                                     a minute ago
3     Change my keyboard mapping to use escape/control    a few seconds ago
```

or for showing all tasks, using a flag (such as -a or --all)

```
$ tasks list -a
ID    Task                                                Created          Done
1     Tidy up my desk                                     2 minutes ago    false
2     Write up documentation for new project feature      a minute ago     true
3     Change my keyboard mapping to use escape/control    a minute ago     false
```


### Complete

To mark a task as done, add in the following method

```
$ tasks complete <taskid>
```

### Delete

The following method should be implemented to delete a task from the data store

```
$ tasks delete <taskid>
```