# Setting up a local development environment
This document will help you set up a local development environment in the style of GitPod. This can be helpful for working with a weak or unreliable internet connection, or if you're worried about running out of compute hours on GitPod. It's also a useful skill for being a programmer in general.

The core components of a development environment are the editor (or IDE), the versioning system (git), and the compiler. To access these tools we can use the terminal.

## Setting up the terminal
This is the step that's most dependent on your operating system. Once we have the terminal configured all the other steps should be roughly the same.

### Mac/Linux
You're already done.

There should already be an application on your computer called `terminal`, all you have to do is launch it. If you're having trouble finding it on Mac, open Applications/Utilities in the Finder and double-click Terminal. If you're having trouble finding it on Linux, try pressing `Ctrl+Alt+t`

### Android
There's a free app called Termux on the play store that gives access to the terminal: https://play.google.com/store/apps/details?id=com.termux

### iPhone/iPad
There's a free app called iSH on the app store that gives access to the terminal: https://apps.apple.com/us/app/ish-shell/id1436902243

### Windows
First we'll need to install the Windows Subsystem for Linux (or WSL), this can be done by opening an elevated command prompt and running `wsl --install`

If that proves difficult, it can also be installed through the GUI:

1. Open Settings in Windows and enable developer mode.
2. Once developer mode is enabled, open the start menu search and type `Bash`
3. It will open the Bash command prompt. Allow it to download the rest automatically.

More detailed instructions can be found here: https://learn.microsoft.com/en-us/windows/wsl/install

### Package Management
Different operating systems can use different package management systems. Practically speaking this means some commands might be different on your machine.

In Windows, Linux, and Android new programs are installed with `apt install`, you may need to add `sudo` to the beginning of the command depending on your permissions, e.g. `sudo apt install`

On iOS new programs are installed with `apk add`

On MacOS new programs are installed with `brew install`  
If you don't already have homebrew, it can be added to your system by running the following command `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

The rest of this document uses `apt install` as a generic command, modify it based on your situation; you may be running `sudo apt install` or `brew install` or `apk add` instead, but the end result should be the same.

## Setting up version control (git)
`apt install git` to install git.

Next you'll need to generate a public key and add it to your GitHub account. Run `ssh-keygen` to generate the key, it's fine to use the defaults, just keep hitting the enter key until it's done.

Copy the public key to your GitHub account:
1. Copy the SSH public key to your clipboard. Run `cat ~/.ssh/id_ed25519.pub` Then select and copy the contents of the file.
2. In the upper-right corner of any page on GitHub, click your profile photo, then click  Settings.
3. In the "Access" section of the sidebar, click  SSH and GPG keys.
4. Click New SSH key or Add SSH key.
5. In the "Title" field, add a descriptive label for the new key. For example, if you're using a personal laptop, you might call this key "Personal laptop".
6. Select authentication for the type of key.
7. In the "Key" field, paste your public key.
8. Click Add SSH key.

You can find more detailed instructions here: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account#adding-a-new-ssh-key-to-your-account

You don't need to do this every time, just when first setting up a new development environment.

## Setting up the editor
There are many editors that can be used: Sublime, NetBeans, VS Code, etc.

You can also use the terminal as your editor by running a program like Vim or Emacs. This is the way really cool programmers do it.

To install vim run `apt install vim`

## Setting up the compiler
Once our code is written we'll need a way to compile it. Run `apt install default-jdk` to install the java development kit.

# Putting it all together
Once your local development environment is configured it's easy to work on assignments with your own device.

## Pull code from github
Run `git clone git@github.com:TheEvergreenStateCollege/upper-division-cs-24-25.git`

## Edit and compile
Move to the code directory: `cd upper-division-cs-24-25/dsa-24au/week-01/code`

Edit a file, e.g. `vim App.java`

Compile the program: `javac *.java`

## Run the program
Run `java App`
