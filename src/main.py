#!/usr/bin/env python3
import argparse
import os
import base64
import json
import re

OUTPUT_DIR = "output"
ASSETS_DIR = os.path.join(OUTPUT_DIR, "_assets", "imgs")
WIDGETS_DIR = os.path.join(OUTPUT_DIR, "Widgets")


def to_snake_case(s):
    # Replace spaces and hyphens with underscores, remove non-alphanumeric characters, and lowercase
    s = re.sub(r'[\s-]+', '_', s)
    s = re.sub(r'[^\w_]', '', s)
    return s.lower()


def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory {path}: {e}")


def write_text_file(path, content):
    if content == None:
        content = ""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file {path}: {e}")


def write_binary_file(path, content):
    try:
        with open(path, "wb") as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing binary file {path}: {e}")


def read_file(file_path):
    """Reads and returns JSON content from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")


def get_files_from_directory(directory):
    """Returns a list of file paths from the specified directory."""
    try:
        return [os.path.join(directory, f) for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f))]
    except Exception as e:
        print(f"Error accessing directory {directory}: {e}")
        return []


def widget_info_to_markdown(widget):
    widget_image_name = None
    widget_image_base64 = None

    for resource in widget.get("resources", []):
        if resource.get("type") == "IMAGE":
            title = resource.get("title", "")
            widget_image_name = title if title.endswith(".png") else title + ".png"
            widget_image_base64 = resource.get("data")
            break  # Process only the first image found

    if widget_image_base64:
        create_directory(ASSETS_DIR)
        image_path = os.path.join(ASSETS_DIR, widget_image_name)
        write_binary_file(image_path, base64.b64decode(widget_image_base64))

    readme_path = os.path.join(OUTPUT_DIR, "README.md")
    try:
        with open(readme_path, "a", encoding="utf-8") as file:
            file.write(f'### {widget["name"]} ')
            file.write(f'[(source code)](<{os.path.join('Widgets', widget["name"], "src", to_snake_case(widget["name"])) + ".json"}>)\n\n')
            if widget.get("description"):
                file.write(f'{widget["description"]}\n\n')
            if widget_image_base64:
                file.write(f'![{widget_image_name}](<_assets/imgs/{widget_image_name}>)\n\n')
            else:
                file.write("NO IMAGE PROVIDED\n\n")
    except Exception as e:
        print(f"Error updating README.md: {e}")


def parse_widget_actions(widget):
    default_config = json.loads(widget["descriptor"]["defaultConfig"])
    actions = default_config.get("actions", {})
    for action_type, action_list in actions.items():
        for action in action_list:
            action_name = action.get("name")
            widget_name = widget["name"]
            action_dir = os.path.join(WIDGETS_DIR, widget_name, "Actions", action_type, action_name)
            if action["type"] == "custom":
                create_directory(action_dir)
                js_file = os.path.join(action_dir, f"{to_snake_case(action_name)}.js")
                write_text_file(js_file, action.get("customFunction", ""))

            if action["type"] == "customPretty":
                create_directory(action_dir)
                html_file = os.path.join(action_dir, f"{to_snake_case(action_name)}.html")
                css_file = os.path.join(action_dir, f"{to_snake_case(action_name)}.css")
                write_text_file(html_file, action.get("customHtml", ""))
                write_text_file(css_file, action.get("customCss", ""))


def parse_and_save_widget(widget):
    widget_name = widget["name"]
    widget_dir = os.path.join(WIDGETS_DIR, widget_name)
    widget_src_dir = os.path.join(widget_dir, "src")

    create_directory(ASSETS_DIR)
    create_directory(widget_dir)
    create_directory(widget_src_dir)

    print("Widget created:", widget_name)

    files_to_write = {
        f"{to_snake_case(widget_name)}.js": widget["descriptor"].get("controllerScript", ""),
        f"{to_snake_case(widget_name)}.css": widget["descriptor"].get("templateCss", ""),
        f"{to_snake_case(widget_name)}.html": widget["descriptor"].get("templateHtml", ""),
        f"{to_snake_case(widget_name)}.settings.json": widget["descriptor"].get("settingsSchema", ""),
        f"{to_snake_case(widget_name)}.datakey.settings.json": widget["descriptor"].get("dataKeySettingsSchema", ""),
    }
    for filename, content in files_to_write.items():
        write_text_file(os.path.join(widget_dir, filename), content)

    # Save the widget's JSON data in the src directory
    widget_json_path = os.path.join(widget_src_dir, f"{to_snake_case(widget_name)}.json")
    write_text_file(widget_json_path, json.dumps(widget))

    parse_widget_actions(widget)
    widget_info_to_markdown(widget)


def main():
    parser = argparse.ArgumentParser(description="Process widget files and create output.")
    parser.add_argument("-d", "--directory", help="Directory containing widget files.")
    parser.add_argument("-f", "--files", nargs="+", help="Individual widget files.")
    args = parser.parse_args()

    files_to_read = set()
    if args.directory:
        files_to_read.update(get_files_from_directory(args.directory))
    if args.files:
        files_to_read.update(args.files)

    if not files_to_read:
        print("No files specified.")
        return

    widgets = []
    for file_path in files_to_read:
        widget_data = read_file(file_path)
        if widget_data:
            widgets.append(widget_data)

    for widget in widgets:
        if "widgetTypes" in widget:
            for bundle_widget in widget["widgetTypes"]:
                parse_and_save_widget(bundle_widget)
            bundle_path = os.path.join(WIDGETS_DIR, f"{widget['widgetsBundle']['alias']}.bundle.json")
            write_text_file(bundle_path, json.dumps(widget))
        else:
            parse_and_save_widget(widget)


if __name__ == "__main__":
    main()
