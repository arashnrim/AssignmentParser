This file explains the context behind why and how AssignmentParser works. In essence, the are steps that are involved with making this program possible include:

1. [compiling the list](#compiling-the-list);
2. [editing the list](#editing-the-list);
3. [parsing the tasks](#parsing-the-tasks); and
4. [syncing the tasks](#syncing-the-tasks).

## Compiling the list

On a daily basis, after the school day has ended, the executive committee of the class spends time to create a compiled list with the daily assignments and homework given for the day. It was great that this list had some form of structure, often with the date preceding the tasks and the subjects of the task being separated from the task with a hyphen. Visualised, the list looks similar to the following:

```
**Date**
Subject - Task
Subject - Task

**Date**
Subject - Task
Subject - Task
Subject - Task

**Date**
Subject - Task
```

Noticing this pattern, an idea came up — since I am using an online to-do list, why not automate the process? An hour and a half later, the initial code that performed the minimal code was done.

## Editing the list

Usually, there are some discrepancies and minor details of the list that I wish to edit. Be it the capitalisation of certain words or omitting assignments that did not apply to me, I will want to spend some (but not too much) time editing the list to make sure that it looks as I expect.

This is where the idea to have the input separated as another file entirely so that I can edit with ease. In the initial creation of the code, this was a considered factor and included. It does not necessarily require a text (.txt) file as an input, but it is the default.

## Parsing the tasks

After passing the input — that is, the list as a file —, the program performs functions that will parse the code into an expected standardised format before syncing it to the Todoist account.

This is hugely arbitrary — I prefer having the tasks in the format `[subject] task` where `subject` is a two-letter capitalised code denoting the subject, and `task` is self-explanatory. Therefore, the functions in the initial creation of the code were designed specially to do just that.

## Syncing the tasks

The final part of the program is to sync the parsed tasks to the Todoist account. After visiting Todoist's helpful documentation on their developer website, it was easy to get started with using its REST API, especially with the Requests module.