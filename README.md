# todocli-python

Implementing project ideas from [here](https://github.com/dreamsofcode-io/goprojects/tree/main)

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

## Notable Packages Used

🧹- `click` simple cli module
- `sqlalchemy` for handling db connections and models
- `sqlite3` Simple in memory db

## Extra Features

- Change the IsComplete property of the Task data model to use a timestamp instead, which gives further information.
- Change from CSV to JSON, JSONL or SQLite
- Add in an optional due date to the tasks
