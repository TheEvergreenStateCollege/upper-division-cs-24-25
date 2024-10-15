The goals of this workshop are:
* To become more comfortable with using GitPod / cloud development environments for all kinds of development including *as an option* for all the threads:
	* Java development in DSA
	* C/C++ development for PDC
	* any other language you wish to use, e.g. Software Engineering projects
* To understand the different parts of setting up any development environment, including a new computer that you've never used before for programming
* To learn how to compile and run Java programs from the command-line
	* javac and java, equivalent to gcc
* To try out code from zyBooks (Counter Demo) in GitPod
* To use a debugger to step through Java code for understanding
	* references, which may point to the same object (aliasing)
	* setting references to null (pointing to no object at all)
	* creating new objects on the heap

You are free to use any development environment which makes sense to you.

## Step 1: See What Workspaces You Have Started

A *workspace* is a virtual server on hardware connected to the internet (and accessible via a website), configured through a container platform, and with a software project preloaded for you to work on as a `git` repository.
* **virtual server**: behaves like a computer that you can see and touch in front of you, with its own operating system, processor, memory, network connection, hostname, but it is actually being simulated by hardware. You can consider this the same as a **workspace**.
* **hardware**: this is usually one of many physical machines owned by a company in a datacenter, but it can also refer to the school's lab computer, a chromebook, or your own laptop. A single physical hardware machine can host zero or more virtual servers.
* **container platform**: this is system software that lets hardware divide up its physical resources into virtual resources for any virtual servers, isolates them from each other, and allows for specific and reproducible versions of software 
* **`git` repository**: a version control system 

In this tutorial, we use GitPod's hardware, we access it at https://gitpod.io and it uses the container platform known as [Docker](). Workspaces have their own operating system: we use a distribution of Linux called Ubuntu because it has beginner-friendly defaults and a package system `apt` that supports popular development software that we use, such as compilers and network tools. When you connect with a single shared workspace that is started by the instructor, that's an example of everyone connecting to the same virtual server.

We don't cover Docker in detail, or hosting your own virtual server for projects, web apps, businesses, or startups, but you can learn more by taking a software infrastructure or cloud engineering class such as [Web Engineering from Winter '24](https://github.com/TheEvergreenStateCollege/upper-division-cs-23-24/tree/main/web-24wi) or the [Docker Curriculum](https://docker-curriculum.com/) .

Because workspaces take resources like electricity, data center space, and support staff to maintain, we are limited to 50 hours of active workspace time each month at GitPod. Let's start by viewing what workspaces we have running (active), any inactive workspaces, and what unsaved changes are in each workspace that we might lose if we delete them.

Click on:
[Your GitPod Dashboard](https://gitpod.io/workspaces)

You may need to login with your GitHub login in GitPod Classic mode (ignore any mention of GitPod Flex for now).

## Step 2: Clean Up

Stop any workspaces you have running that have unsaved data.

If any workspaces have no unsaved changes, they are safe to delete.

We're going to create a single new workspace now, that will load the current Docker environment from the class monorepo . You can see exactly what software we install our workspace by examining the Dockerfile

https://github.com/TheEvergreenStateCollege/upper-division-cs-24-25/blob/main/.gitpod.Dockerfile

In the future, you want to limit yourself to just one workspace with unsaved changes, that you'll use for in-class workshops like this, or your final project if you wish, or work from other classes.

You'll continue to use zyBooks to submit Java labs, but now you'll understand what zyBooks servers are doing behind-the-scenes to compile and run your Java code.

Also be sure to stop your GitPod workspace at the end of class to save your 50 hours each month.
## Step 3: Know What Directory You Are In
In this class, we use the UNIX command-line and interact with it via a shell called `bash`.
The effect of commands that we run depend on *our current working directory* within a hierarchical filesystem that begins at root, named `/` (a leading slash).

Think of it as a "You Are Here" cursor on a map that describes your current location, for example, when you're at the mall or hiking in a forest. 

The terminal is the pane at the bottom of your GitPod workspace, below your text editor to the left of the file explorer pane. It has a *prompt* with a blinking cursor where text will next appear when you type commands, which is bash is shown as a dollar sign followed by space

```
$ 
```

You can find out what directory you are in at any time by using the `pwd`, or "print working directory" command

```
$ pwd
```

By default, we start out in a `git` repository that has been cloned for us in the root directory called

`/workspace/upper-division-cs-24-25`

For today's exercise, we want to change into the subdirectory for Core DSA, called `dsa-24au`, and a subsubdirectory inside that called `week-03`, and a subsubsubdirectory inside that called `code`. (We'll just called any directory a subdirectory from now on, but keep in mind that it is inside a parent directory, and that parent could have its own parent, all the way back to the filesystem root).

Try typing out the following, and as you type, feel free to press the tab key once to autocomplete any options if you start typing a prefix that uniquely identifies a file. If nothing happens after you press tab once, you might have multiple endings to a prefix, and you can press tab twice to see your options.
```
cd dsa-24au/week-03/code
```
Press enter to change the current working directory, and then you can end `pwd` again to verify that you're in a new directory.

```
$ pwd
`/workspace/upper-division-cs-24-25/dsa-24au/week-03/code`
```
Look at files in the current directory, their size in bytes, who owns them (you the `gitpod` user), read/write permissions, and other information related to how to use them.
```
ls -lh
```
## Step 4: Make Sure Your Java Development Tools are in Your Path

```
which java
```

```
which javac
```
## Step 5: Compile Java Code

```
javac *.java
```
Inspect the files produced.
```
ls -lh
```
## Step 6: Configure JAVA_HOME

Open Settings with the cogwheel icon.
![image](https://github.com/user-attachments/assets/28321342-5fc9-4d54-8d9b-e8744e90bf35)

Open the file `settings.json` (instructions to follow on how to find this)

Search for "java.configuration"
Choose "Installed JDKs",
Find and click "edit settings.json"

https://canvas.evergreen.edu/courses/6729/assignments/126587
