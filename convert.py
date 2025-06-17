import json
import sys
import xml.etree.ElementTree as ET

def json_to_xml(value, name=None):
    if isinstance(value, dict):
        elem = ET.Element("object")
        for k, v in value.items():
            child = json_to_xml(v, k)
            if child is not None:
                elem.append(child)
        if name:
            elem.set("name", name)
        return elem
    elif isinstance(value, list):
        elem = ET.Element("array")
        for item in value:
            child = json_to_xml(item)
            if child is not None:
                elem.append(child)
        if name:
            elem.set("name", name)
        return elem
    elif isinstance(value, str):
        elem = ET.Element("string")
        elem.text = value
    elif isinstance(value, bool):
        elem = ET.Element("boolean")
        elem.text = "true" if value else "false"
    elif isinstance(value, (int, float)):
        elem = ET.Element("number")
        elem.text = str(value)
    elif value is None:
        elem = ET.Element("null")
        return elem
    else:
        return None

    if name:
        elem.set("name", name)
    return elem

def convert_json_to_xml(input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)

    root = json_to_xml(data)
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input.json> <output.xml>")
    else:
        convert_json_to_xml(sys.argv[1], sys.argv[2])
