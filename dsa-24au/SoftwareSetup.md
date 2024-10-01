# Software Setup

You will only need to go through this Software Setup once at the beginning of
Data Structures & Algorithms. However, if you have never used GitHub and GitPod
before, or if you need a refresher, please budget plenty of time to complete these
steps. You'll need them to complete Assignment 1 in the first week,
as well as all the other assignments.

As you read through, be on the lookout for mistakes, discrepancies, bugs, or anything
that doesn't work out the way you expect. Congrats, you've found an issue that 
you can use to complete Step 9 of the Cloud IDE setup below. 

## GitHub

You'll need to sign up for a GitHub account.

### 1. Go to GitHub

In your browser, enter the url https://github.com

Click on "Register" to create a new account,
or "Login" if you already have an account.

Verify with your phone number.

### 2. Request to be added to class monorepo
Go to https://github.com/TheEvergreenStateCollege/upper-division-cs-24-25/issues

Click the "New issue" green button and create a new issue with the title
"Add <your-username> as maintainer" and with the label `admin`.
Assign it to ten of your classmates.

You can paste the following body into a new issue:
```
This issue is part of [SoftwareSetup.md](dsa-23au/SoftwareSetup.md).
I would like to be a maintainer of our learning organization,
responsible for surfacing any problems I can find, helping my classmates,
and creating a fun and safe learning environment.
I will do my best to learn how to create pull requests, merge branches,
give code reviews, write and refactor Java code in this monorepo,
and work on resolving issues and pull requests opened by my classmates.
```


## Cloud IDE 

We will be using GitPod, a online integrated development environment (IDE) that can be
accessed from any web browser, allowing you to easily work on lab computers or on your
home machines.

### 1. Go to GitPod

In your browser, enter the URL https://gitpod.io

This is the first URL you'll enter into a web browser
each time you sit down at a computer to work on this class.

If you've chosen to download and install Desktop IDEs like VSCode or IntelliJ
to your laptop, with the appropriate Gitpod plugins, you can open those IDEs
directly.

Choose to login via your GitHub account, which you've created or logged into
as part of the previous section.

### 2. Link Your LinkedIn Account

There is free plan allowing up to 50 hours per month of use if you create and link
your [LinkedIn](https://linkedin.com) account. You may wish to do this to connect
with alumni, recruiters, or professionals in the field or specialty that you are
interested in working in.

<img width="647" alt="image" src="https://github.com/TheEvergreenStateCollege/upper-division-cs/assets/148553/a88ddaef-3e6b-4144-b3ef-77db384c63ca">

### 3. Answer the Survey 

Answer some preliminary questions about our use of Gitpod for this class.
You can adjust your answers to suit your preferences, it won't affect your development experience.

<img width="625" alt="image" src="https://github.com/TheEvergreenStateCollege/upper-division-cs/assets/148553/9dbdf8bb-0bc8-4cba-8543-25af7edea404">

### 4. Create a Workspace

Since this is probably your first time using GitPod for this class,
click on "New workspace" and copy and paste the class monorepo

https://github.com/TheEvergreenStateCollege/upper-division-cs-24-25

Occasionally, when the Dockerfile has been changed,
GitPod will need to build the image from the last layer changed.

This may take up to a few minutes the first time, in which case you will see
an image like the following. It will be near instance to start a new
workspace thereafter.

<img width="966" alt="image" src="https://github.com/TheEvergreenStateCollege/upper-division-cs/assets/148553/ac68ebea-23bc-4a59-a3c6-a35e1f9abaf4">


### 5. Open GitPod in Your Browser

Choose "Open in Browser". This will open up VSCode in your browser.

<img width="498" alt="image" src="https://github.com/TheEvergreenStateCollege/upper-division-cs/assets/148553/3caf24e4-7478-4438-ada7-24114b3d1efe">

<img width="900" alt="image" src="https://github.com/TheEvergreenStateCollege/upper-division-cs/assets/148553/e78511b9-f307-4af5-bbc8-4e5908963583">

### 6. Enable Write Permissions

Enable permissions in Gitpod's integrations for Github / Bitbucket / Gitlab by navigating to this URL
https://gitpod.io/user/integrations

Next to the "GitHub" integration, click on the three dots and choose "Manager this on github.com"

<img width="1103" alt="image" src="https://github.com/TheEvergreenStateCollege/upper-division-cs/assets/148553/6e2b9019-00b3-4b5f-bd4e-4073f28b6551">

<img width="703" alt="image" src="https://github.com/TheEvergreenStateCollege/upper-division-cs/assets/148553/dfe3093a-93c5-4441-9ec3-00798bb29dfb">

<img width="655" alt="image" src="https://github.com/TheEvergreenStateCollege/upper-division-cs/assets/148553/b7f844af-3fc0-404c-b663-14c5f5fed97f">

### 7. Set your Git Config Email

Go to your `gitpod.io` environment variable settings at https://gitpod.io/user/variables.
On this page add two new variables with the keys being
`GIT_AUTHOR_EMAIL` and `GIT_COMMITER_EMAIL` and value being your github privacy email address. You will need to set a scope for this environment variables.
`*/*` can be used if you want these emails to be applied to all workspaces opened in gitpod,or they could be set to `TheEvergreenStateCollege/upper-division-cs`. 

### 8. Make sure you have tools in your $PATH

```
$ which java
/opt/graalvm-community-openjdk-20.0.2+9.1/bin/java
$ which mvn
/opt/apache-maven-3.9.4/bin/mvn
```
```
source ./scripts/.shrc
```

### 9. Go to your GitHub settings

In your GitHub email settings:
https://github.com/settings/emails

and copy your private, "no-reply" email address that GitHub generated for you,
to avoid leaking your real email address to the public.

It will look similar to mine, which is
`148553+learner-long-life@users.noreply.github.com`

Copy this and save it for the next step.

### 10. Create a configuration script

You'll run this script the first time you start up GitPod using this repository (below).

In GitPod, create a new file in the path `/workspace/upper-division-cs/dsa-23au/scripts/git-config.sh`
which you can do by clicking the file icon with a plus sign show in the screenshot below

<img width="447" alt="image" src="https://github.com/TheEvergreenStateCollege/upper-division-cs/assets/148553/07fac582-5576-47e9-8a64-b089f8a440bb">

<img width="1000" alt="image" src="https://github.com/TheEvergreenStateCollege/upper-division-cs/assets/148553/2c97e315-ba12-46cf-9631-70d97e121895">

Add these contents to the file, being sure to replace your private email address 
```
#!/bin/sh

# Enable us to push, through email privacy features
git config --global user.email 148553+learner-long-life@users.noreply.github.com
```

Don't worry, this is not a real email address, and this is a private repo, so you are not revealing anything
unsafe by saving it here.

### 11. Update this Document

Test that everything works by making a change to these instructions, adding
any corrections, insights, jokes, comments, or memes that you think will help future students.

If you are looking for a beginner-friendly change to make,
check out [any open Issues for this GitHub repository](https://github.com/TheEvergreenStateCollege/upper-division-cs/issues).

The file is located at

```
./dsa-23au/SoftwareSetup.md
```

Right-click the tab in GitPod and choose "Open Preview"

All documentation in this class is written using Markdown, a simplified formatting language that is
meant to be plaintext and human-readable.

You can read more about [using Markdown here](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### 12. Add, Commit, Push

After making your changes, you will perform the `version control dance` of hackers everywhere.

First you will *stage your changes for commit*. This helps separate changes that are ready
and others which you may still be working on. In our case, we want to stage our changes to
`SoftwareSetup.md`, since we want others to receive changes and corrections,
but we will ignore our changes to `git-config.sh`, since it contains a no-reply email address
that is specific to just us.

```
git add SoftwareSetup.md
```

Next, you will *check the status* to see that only the files you meant to stage are going to be committed.
You will probably see two files to change.

```
git status
```

Then you'll commit the file that is staged.
```
git commit
```

This will bring up a temporary text editor pane in VSCode where you can type a brief,
typically one-sentence message summarizing the changes you made.

```
git push
```
