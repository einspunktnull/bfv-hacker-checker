# bfv-hacker-checker

Choose players of current match for a cheater check via bfvhackers.com

## Purpose of this application and how it works

This is an open-source **Windows-only** application written with
[Python programming language](https://en.wikipedia.org/wiki/Python_(programming_language)).
In the Battlefield game it makes a screenshot of an area around your mouse pointer and recognize the Playername via
[OCR](https://en.wikipedia.org/wiki/Optical_character_recognition). This is done by the bundled open-source software
[Tesseract](https://en.wikipedia.org/wiki/Tesseract_(software)).
When a playername was detected it shows up the bfvhackers.com website
with the detected playername.

## Issues

The detection is not perfect. The tesseract pretrained OCR model is not made for the
font `Futura PT Medium` which is used in Battlefield V.
Maybe I will train a specific model for better detection, maybe not.

## Installation

There is no installation needed. Just unzip the `bfv-hacker-checker.zip`
to a location of your choice. This application is portable.

## How to use

Just run the `bfv-hacker-checker.exe`.
To trigger the Hacker Lookup, hold a specified key (default=`ctrl_l`)
and click on playername in the Scoreboard.
The trigger key can be changed in the config file

## Configuration

There are several config options defined in the `config.ini` which can be changed.

| Section   | Option               | Type      | Description                                                                                                                                                                                                                                                                                                                                   | 
|-----------|----------------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `app`     | `url`                | `String`  | The url which is called, pattern: `<url>?name=<playername>`                                                                                                                                                                                                                                                                                   |
| `app`     | `always_on_top`      | `Bool`    | Application windoww on top of all open windows                                                                                                                                                                                                                                                                                                |
| `app`     | `clear_data_dir`     | `Bool`    | Clear the data dir on startup. Only applied/needed if `debug` option <br/>is set to `True`                                                                                                                                                                                                                                                    |
| `app`     | `debug`              | `Bool`    | Show debug messages and create temporary images in the `data` directory                                                                                                                                                                                                                                                                       |
| `user`    | `default_playername` | `String`  | Initial Playername which is looked for (Makes no sense - just for fun)                                                                                                                                                                                                                                                                        |
| `user`    | `hotkey`             | `String`  | The trigger Key possible is <br/>`alt,alt_l,alt_r,alt_gr,backspace,caps_lock,cmd,cmd_l,`<br/>`cmd_r,ctrl,ctrl_l,ctrl_r,delete,down,end,enter,esc,`<br/>`f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,`<br/>`home,left,page_down,page_up,right,shift,shift_l,shift_r,`<br/>`space,tab,up,insert,menu,num_lock,pause,`<br/>`print_screen,scroll_lock` |
| `user`    | `poi_width`          | `Integer` | The rectangular area width around the mousepointer in pixels                                                                                                                                                                                                                                                                                  |
| `user`    | `poi_height`         | `Integer` | The rectangular area height around the mousepointer in pixels                                                                                                                                                                                                                                                                                 |
| `logging` | `level`              | `String`  | At which level the messages should be included in the logfile.possibs:<br/>`CRITICAL,FATAL,ERROR,WARNING,INFO,DEBUG,NOTSET`                                                                                                                                                                                                                   |
| `logging` | `file`               | `String`  | location where the logfile is written. if omitted no logfile is written                                                                                                                                                                                                                                                                       |

## Development Notes

### Requirements

- Python >=3.10,<3.12
- [Poetry](https://python-poetry.org)

### Create virtual env

```shell
poetry install
```

### Build

```shell
poe build
```