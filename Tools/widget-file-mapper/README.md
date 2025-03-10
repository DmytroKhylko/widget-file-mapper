# CLI tool to map Thingsboard widgets to a file system

## User manual

### Description

CLI tool that maps Thingsobard widgets to a file structure

```txt
output/
    ├── _assets/                       # Folder with additional resources needed for the Markdown
    │   └── imgs/                      # Folder for Markdown images
    ├── Widgets/
    │   ├── [widgets_bundle].bundle.json         # Bundle file for all widgets (if such exists, recommended to use naming convention project_widgets_bundle.json)
    │   └── [Widget Name]/
    │       ├── src/
    │       │   └── [widget_name].json       # JSON widget configuration
    │       ├── [widget_name].js         # JavaScript code for the widget
    │       ├── [widget_name].html       # HTML markup for the widget
    │       ├── [widget_name].css        # CSS styles for the widget
    │       ├── [widget_name].settings.json    # Widget settings schema
    │       ├── [widget_name].datakey.settings.json    # Widget datakey settings schema
    │       └── Actions/                # Folder for all widget actions
    │           ├── [actionType]
    │           │   └── [Action Name]/      # Each action in its own folder
    │           │       ├── [action_name].js   # JavaScript code for the action
    │           │       ├── [action_name].html # HTML for the action (if needed)
    │           │       └── [action_name].css  # CSS for the action (if needed)
    │
    └── README.md                   # README file which contains project description, design pictures and more TODO: think through the strcture of the README
```

The tool automatically distinguishes between widget and widget bundle. In case with widget bundle the tool creates all the widgets separately

The tool creates `output` directory in directory where the tool was called

### Options

`-d`

`--directory`

Specifies a directory to get all the `.json` files from

Usage:

```sh
python main.py -d Downloads/
```

---

`-f`

`--files`

Specifies an array of `.json` files to use

Usage:

```sh
python main.py -f widget_1.json widget_2.json
```

## IMPORTANT

- This is a work in progress tool which primary goal is to ease the process of saving widgets to the git

- Currently tested versions:
  - 3.9.0

- As of this moment the tool doesn't handle repetitive names and overwrites to the last processed
