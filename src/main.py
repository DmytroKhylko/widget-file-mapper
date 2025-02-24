#!/usr/bin/env python3
import argparse
import os
import base64
import json
import re

def to_snake_case(s):
    # Replace spaces and hyphens with underscores
    s = re.sub(r'[\s-]+', '_', s)
    # Remove any characters that are not alphanumeric or underscores
    s = re.sub(r'[^\w_]', '', s)
    return s.lower()

def read_file(file_path):
    """Reads and prints the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file = f.read()
            return json.loads(file)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def get_files_from_directory(directory):
    """Returns a list of file paths from the specified directory."""
    try:
        return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except Exception as e:
        print(f"Error accessing directory {directory}: {e}")
        return []


def widget_info_to_markdown(widget):
    widget_image_name = None
    widget_image_base64 = None
    for resource in widget['resources']:
        if resource['type'] == 'IMAGE':
            widget_image_name = resource['title'] if resource['title'].endswith(".png") else resource['title'] + ".png"
            widget_image_base64 = resource['data']
    try:
        if (widget_image_base64):
            with open(f'output/_assets/imgs/{widget_image_name}', "wb") as file:
                file.write(base64.b64decode(widget_image_base64))

        with open(f'output/README.md', "a", encoding="utf-8") as file:
            file.write(f'### {widget['name']}\n\n')
            if (widget['description']):
                file.write(f'{widget['description']}\n\n')
            if (widget_image_base64):
                # file.write(f'![{widget_image_name}](_assets/imgs/{quote(widget_image_name)})\n\n')
                file.write(f'![{widget_image_name}](<_assets/imgs/{widget_image_name}>)\n\n')
            else:
                file.write(f'NO IMAGE PROVIDED\n\n')


    except Exception as e:
        print(e)

def parse_widget_actions(widget):
    default_config = json.loads(widget['descriptor']['defaultConfig'])
    if ('actions' in default_config.keys()):
        widget_actions = default_config['actions']
        for widget_action_type in widget_actions:
            for widget_action in widget_actions[widget_action_type]:
                if widget_action['type'] == 'custom':
                    try:
                        os.makedirs(f'output/Widgets/{widget['name']}/Actions/{widget_action_type}/{widget_action['name']}', exist_ok=True)
                    except FileExistsError as e:
                        print(e)
                    except Exception as e:
                        print(e)

                    try:
                        with open(f'output/Widgets/{widget['name']}/Actions/{widget_action_type}/{widget_action['name']}/{to_snake_case(widget_action['name'])}.js', "w", encoding="utf-8") as file:
                            file.write(widget_action['customFunction'])
                    except Exception as e:
                        print(e);
                elif widget_action['type'] == 'customPretty':
                    try:
                        os.makedirs(f'output/Widgets/{widget['name']}/Actions/{widget_action_type}/{widget_action['name']}', exist_ok=True)
                    except FileExistsError as e:
                        print(e)
                    except Exception as e:
                        print(e)

                    try:
                        with open(f'output/Widgets/{widget['name']}/Actions/{widget_action_type}/{widget_action['name']}/{to_snake_case(widget_action['name'])}.js', "w", encoding="utf-8") as file:
                            file.write(widget_action['customFunction'])
                        with open(f'output/Widgets/{widget['name']}/Actions/{widget_action_type}/{widget_action['name']}/{to_snake_case(widget_action['name'])}.html', "w", encoding="utf-8") as file:
                            file.write(widget_action['customHtml'])
                        with open(f'output/Widgets/{widget['name']}/Actions/{widget_action_type}/{widget_action['name']}/{to_snake_case(widget_action['name'])}.css', "w", encoding="utf-8") as file:
                            file.write(widget_action['customCss'])
                    except Exception as e:
                        print(e);


def parse_and_save_widget(widget):
    try:
        os.makedirs(f'output/_assets/imgs', exist_ok=True)
        os.makedirs(f'output/Widgets/{widget['name']}', exist_ok=True)
        os.makedirs(f'output/Widgets/{widget['name']}/src/', exist_ok=True)
        print('Widget created:', widget['name'])
    except FileExistsError as e:
        print(e)
    except Exception as e:
        print(e)

    try:
        with open(f'output/Widgets/{widget['name']}/{to_snake_case(widget['name'])}.js', "w", encoding="utf-8") as file:
            file.write(widget['descriptor']['controllerScript'])
    except Exception as e:
        print(e);

    try:
        with open(f'output/Widgets/{widget['name']}/{to_snake_case(widget['name'])}.css', "w", encoding="utf-8") as file:
            file.write(widget['descriptor']['templateCss'])
    except Exception as e:
        print(e);

    try:
        with open(f'output/Widgets/{widget['name']}/{to_snake_case(widget['name'])}.html', "w", encoding="utf-8") as file:
            file.write(widget['descriptor']['templateHtml'])
    except Exception as e:
        print(e);

    try:
        with open(f'output/Widgets/{widget['name']}/{to_snake_case(widget['name'])}.settings.json', "w", encoding="utf-8") as file:
            file.write(widget['descriptor']['settingsSchema'])
    except Exception as e:
        print(e);

    try:
        with open(f'output/Widgets/{widget['name']}/{to_snake_case(widget['name'])}.datakey.settings.json', "w", encoding="utf-8") as file:
            file.write(widget['descriptor']['dataKeySettingsSchema'])
    except Exception as e:
        print(e);

    try:
        with open(f'output/Widgets/{widget['name']}/src/{to_snake_case(widget['name'])}.json', "w", encoding="utf-8") as file:
            file.write(json.dumps(widget))
    except Exception as e:
        print(e);

    # print(widget['descriptor']['defaultConfig'])

    parse_widget_actions(widget)
    widget_info_to_markdown(widget)

def main():
    parser = argparse.ArgumentParser(description="Read and print the contents of files.")
    parser.add_argument("-d", "--directory", help="Specify a directory to read all files from.")
    parser.add_argument("-f", "--files", nargs="+", help="Specify individual files to read.")

    args = parser.parse_args()

    files_to_read = set()  # Using a set to avoid duplicate file processing

    if args.directory:
        files_to_read.update(get_files_from_directory(args.directory))

    if args.files:
        files_to_read.update(args.files)

    if not files_to_read:
        print("No files specified.")
        return

    widgets = []
    for file in files_to_read:
        widgets.append(read_file(file))

    for widget in widgets:
        if ('widgetTypes' in widget.keys()):
            for bundleWidget in widget['widgetTypes']:
                parse_and_save_widget(bundleWidget)
            try:
                with open(f'output/Widgets/{widget['widgetsBundle']['title']}.bundle.json', "w", encoding="utf-8") as file:
                    file.write(json.dumps(widget))
            except Exception as e:
                print(e);
        else:
            parse_and_save_widget(widget)

if __name__ == "__main__":
    main()
