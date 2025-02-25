# How to use github from terminal

## Cloning the Repository

Move to the wanted folder

```sh
cd .\Documents\Python\My_Project
```
Then clone the desired repository on your folder
```sh
git clone https://github.com/user/repo_name.git
```

## Creating a branch

### Why Work in a Branch?
Working in a branch allows you to develop new features or fix bugs without affecting the main codebase. This keeps the main branch stable while enabling multiple developers to work on different tasks simultaneously. Once the work is complete and tested, the branch can be merged back into the main branch safely.

First check where are we:
```sh
git branch
```
It will tell me if I am in the main or not, and it will enlist all the branches.\
If I want to **create** (and to move to) a non-existing branch, I will use the command
```sh
git checkout -b branch_name
```
This command will give an **error** if the branch already exists.\ 
In this case I need to use:
```sh
git switch branch_name
```

---

## Pushing a Branch

After making changes in your local branch (on your pc), you need to push your work to GitHub. First, check the status of your changes:

```sh
git status
```

Then stage and commit the changes:

```sh
git add .
```
The dot represents "current directory" and tells Git to stage all changes (=add all modifications) (new files, modified files, deleted files) within the current directory and its subdirectories.
```sh
git commit -m "Description of the changes"
```
Committing is helpful when we are looking for a previous version: so we do not have to check each change in each file of that version.

Now push the branch to GitHub:

```sh
git push
```

---

## Fetching and Merging Before Pushing to Main

When working in a branch, you don’t need to worry about overwriting others’ work. However, **before merging into `main`, you should update your branch to avoid conflicts.**

First, fetch (get/download) the latest changes from GitHub:

```sh
git fetch origin
```

Then merge the latest `main` branch into your branch:

```sh
git merge origin/main
```

If there are conflicts (can happen if working on the same file), Git will notify you, and you will need to resolve them manually before proceeding. Example:\
branch1: print("Hello world")\
branch2: print("Goodbye world")\
You have to decide if to keep branch1, branch2 or to combine them.

Finally, after ensuring your branch is up-to-date, you can merge it into `main`:

```sh
git checkout main
git merge branch_name
```

Then push the updated `main` branch to GitHub:

```sh
git push origin main
```

This ensures that you don’t overwrite colleagues' changes while keeping everything synchronized.







