**Pip-Boy 3000 Mk V**

RobCo Custom Unified Operating System (`C-UOS`)

A custom firmware for the [Pip-Boy 3000 Mk V][link-twc-pipboy] by [The Wand
Company][link-twc] that replaces the stock firmware with new user interfaces and
additional features.

This projects goal is to more closely resemble a Fallout Pip-Boy 3000 interface 
as a custom variation of the [UOS][link-uos].

## Software overview

### Espruino interpreter

Espruino is a JavaScript interpreter for microcontrollers, allowing you to write
code in JavaScript and run it directly on the hardware. The [Pip-Boy 3000 Mk
V][link-twc-pipboy] uses Espruino to run the `C-UOS` firmware.

### Firmware (`C-UOS`)

The `C-UOS` firmware is a custom operating system designed for the [Pip-Boy 3000
Mk V][link-twc-pipboy]. It provides a custom user interface and various
functionalities not available in the stock firmware. The firmware is written in
JavaScript and runs on the Espruino interpreter.

## Development Environment Setup (Windows)

### Core

1.  Install [**Git**][link-git] for version control and submodules.

2.  Clone the repository and its submodules:

    ```sh
    git clone https://github.com/CodyTolene/pip-boy-3000-mk-v.git
    cd pip-boy-3000-mk-v
    git submodule update --init --recursive
    ```

### Espruino Build Environment

https://github.com/espruino/Espruino/blob/master/README_Building.md

1.  Install tools:

    - [**MSYS2**][link-msys2] for running the tools on Windows.

2.  Open a new **MSYS2** terminal in `/espruino` (or `cd espruino`) and update
    the package database:

    ```sh
    pacman -Syu
    ```

3.  Install dependencies:

    ```sh
    pacman -S git make python \
        mingw-w64-ucrt-x86_64-gcc \
        mingw-w64-ucrt-x86_64-dfu-util \
        mingw-w64-ucrt-x86_64-arm-none-eabi-gcc

    ```

4.  Verify toolchain:

    ```sh
    which arm-none-eabi-gcc # Should output `/ucrt64/bin/arm-none-eabi-gcc`
    ```

    > ![Info][img-info] You can verify version with
    > `arm-none-eabi-gcc --version`.

5.  Build the Espruino firmware for the Pip-Boy:

    ```sh
    make clean
    BOARD=PIPBOY RELEASE=1 make
    ```

    The compiled firmware binary will be located in:

    ```
    espruino/Espruino*.bin
    ```

    This is the **low-level interpreter firmware** that runs your custom JS
    code.

6.  Flash the firmware to the Pip-Boy 3000 Mk V:

    - Connect the Pip-Boy via **USB-C**.
    - Boot into DFU mode (hold `PLAY` while connecting power).
    - Use `dfu-util` to flash:

      ```sh
      dfu-util -a 0 -s 0x08000000:leave -D Espruino*.bin
      ```

7.  Install the [Espruino CLI](https://www.npmjs.com/package/espruino) for
    uploading and testing JS firmware:

    ```sh
    npm install -g espruino
    ```

8.  Upload and test your **JavaScript firmware** (`C-UOS`) using the Espruino
    CLI:

    ```sh
    espruino --port /dev/ttyACM0 --baud 115200 --no-ble \
             --board PIPBOY src/main.js
    ```

    > **Tip:** On Windows, the port will appear as `COMx`.

9.  (Optional) Enable live development:

    - Use `espruino --watch` to auto-upload changes.
    - Log output via serial to observe memory usage and debug messages.

### JavaScript UI Firmware (`C-UOS`) Build Environment

1.

### Changes and contributions

Make sure to undo any changes to submodules before committing. You can do this
by running:

```sh
git submodule foreach --recursive git clean -fdx
```

<!-- LINKS -->

[link-arm-gnu-toolchain]:
  https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads
[link-git]: https://git-scm.com/downloads
[link-github-issues]: https://github.com/CodyTolene/pip-boy-3000-mk-v/issues
[link-msys2]: https://www.msys2.org/
[link-node-js]: https://nodejs.org/en/download
[link-pipboy.py]:
  https://github.com/espruino/Espruino/blob/master/boards/PIPBOY.py
[link-python]: https://www.python.org/downloads/
[link-twc-pipboy]: https://www.thewandcompany.com/fallout-pip-boy/
[link-twc]: https://www.thewandcompany.com
[link-uos]: https://fallout.fandom.com/wiki/Unified_Operating_System

<!-- IMAGES -->

[img-info]: .github/images/ng-icons/info.svg
[img-warn]: .github/images/ng-icons/warn.svg
