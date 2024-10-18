# Homebrew Without Root
This guide briefly goes over the steps required to add homebrew to your home directory on MacOS, which will allow it to be used without root access to the computer. Homebrew is useful for installing many essential tools for programming, such as git and Python. Once installed homebrew can be accessed with the `brew` command. [Read more about Homebrew here.](https://docs.brew.sh/)

1. Open a new terminal window or run `cd` to get to your home directory.
2. Download and extract the homebrew files:
    ```
    mkdir homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew
    ```
3. Add homebrew/bin to the system path:
    ```
    echo "export PATH=$HOME/homebrew/bin:$PATH" >> ~/.bash_profile && source ~/.bash_profile
    ```
4. Test the installation by running `brew update`
