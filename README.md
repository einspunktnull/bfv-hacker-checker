# Battlefield V Hacker Checker

Choose players of current match for a cheater check via the terrific [bfvhackers.com](https://bfvhackers.com/) website.
(Thx for the great work)

[DEMO: Battlefield V Hacker Checker in Action](https://www.youtube.com/watch?v=5wt4q2CYWj4)

## Purpose of this application and how it works

This App is a Microsoft Windows (Only Windows 10 tested) application written with the
[Python programming language](https://en.wikipedia.org/wiki/Python_(programming_language)).
In the Battlefield game it makes a screenshot of an area around your mouse pointer and recognize the Playername via
[OCR](https://en.wikipedia.org/wiki/Optical_character_recognition). This is done by the bundled open-source software
[Tesseract](https://en.wikipedia.org/wiki/Tesseract_(software)).
When a playername was detected it shows up the bfvhackers.com website with the detected playername.
NOTE: for innofficial Linux see [Inofficial Linux Support](#inofficial-linux-support) section

## IMPORTANT - Known Issues

- Anti-Virus/Malware Software like Windows Defender maybe classify this app as malware. Maybe because
  it is listening for global key inputs (for trigger the playername detection). This behaviour seems to be interpreted
  as dangerous keylogger pattern. So if u want to use it set an exception rule for this app.

- The detection is not perfect. The tesseract pretrained OCR model is not made for the
  font (Futura PT Medium ?, DIN 1451 ?) which is used in Battlefield V.
  Maybe I will train a specific model for better detection, maybe not. Currently, it is good/bad as is.

## Installation

There is no installation needed. Just unzip the `bfv-hacker-checker.zip`
to a location of your choice. This application is portable.

## Download Release

[Download a release here](https://github.com/einspunktnull/bfv-hacker-checker/releases)

## How to use

Just run the `bfv-hacker-checker.exe`.
To trigger the Hacker Lookup, hold a specified key (default=`ctrl_l`)
and click on playername in the Scoreboard.
The trigger key can be changed in the config file

## Configuration

There are several config options defined in the `config.ini` which can be changed.

| Section   | Option               | Type      | Description                                                                                                                                                                                                                                                                                                                                     | 
|-----------|----------------------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `app`     | `url`                | `String`  | The url which is called, pattern: `<url>?name=<playername>`                                                                                                                                                                                                                                                                                     |
| `app`     | `always_on_top`      | `Bool`    | Application windoww on top of all open windows                                                                                                                                                                                                                                                                                                  |
| `app`     | `debug`              | `Bool`    | Enable logging and create temporary images in the `data` directory                                                                                                                                                                                                                                                                              |
| `app`     | `theme`              | `String`  | Set global Appearance. Possibs;  `none,auto,dark,light`                                                                                                                                                                                                                                                                                         |
| `user`    | `default_playername` | `String`  | Initial Playername which is looked for (Makes no sense - just for fun)                                                                                                                                                                                                                                                                          |
| `user`    | `hotkey`             | `String`  | The trigger key value can be: <br/>`alt,alt_l,alt_r,alt_gr,backspace,caps_lock,cmd,cmd_l,`<br/>`cmd_r,ctrl,ctrl_l,ctrl_r,delete,down,end,enter,esc,`<br/>`f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,`<br/>`home,left,page_down,page_up,right,shift,shift_l,shift_r,`<br/>`space,tab,up,insert,menu,num_lock,pause,`<br/>`print_screen,scroll_lock` |
| `user`    | `poi_width`          | `Integer` | The rectangular area width around the mousepointer in pixels                                                                                                                                                                                                                                                                                    |
| `user`    | `poi_height`         | `Integer` | The rectangular area height around the mousepointer in pixels                                                                                                                                                                                                                                                                                   |
| `logging` | `level`              | `String`  | At which level the messages should be included in the logfile. possibs:<br/>`CRITICAL,FATAL,ERROR,WARNING,INFO,DEBUG,NOTSET`                                                                                                                                                                                                                    |

## Inofficial Linux Support

Since Battlefield V (PC) is a Windows Game, there is no need to support Linux.
However, It is possible to run [Batttlefield V with Linux using Lutris](https://lutris.net/games/battlefield-v/).
I want to use it on Linux because it is my favorite platform and I made it runnable on Manjaro Linux (Arch).
Ther will be no official precompiled binaries. So u have to build it ur own. See [Development Notes](#development-notes)
section.

## Development Notes

### Requirements

- [Python](https://www.python.org/) >=3.10,<3.12
- [Poetry](https://python-poetry.org)

### Create virtual environment

```shell
poetry install
```

### Build and Run

The **build** and **run** tasks are done by a tool called [Poe the Poet](https://github.com/nat-n/poethepoet).
Before u can use them u have to enable a **Poetry-Shell** with following command:

```shell
poetry shell
```

and then u can execute the following commands inside this shell

#### Build

```shell
poe build
```

#### Run

```shell
poe app
```