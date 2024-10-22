# Installing Java with Homebrew

1. Make sure homebrew is installed, you can run `brew info` as a test.
2. Install Java by running:
    ```
    brew install java
    ```
3. Link OpenJDK to your Library by running:
    ```
    mkdir $HOME/Library/Java $HOME/Library/JavaVirtualMachines && ln -sfn $HOME/homebrew/opt/openjdk/libexec/openjdk.jdk $HOME/Library/Java/JavaVirtualMachines/openjdk.jdk
    ```
