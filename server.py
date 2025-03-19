from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import xml.etree.ElementTree as ET
import time

DATABASE = "notes.xml"
PORT = 1000
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): # Multithreaded queries
    pass

def init_db():
    try:
        tree = ET.parse(DATABASE)
        return tree
    except FileNotFoundError:
        root = ET.Element("data")
        tree = ET.ElementTree(root)
        tree.write(DATABASE)
        return tree
    except Exception as e:
        print(f"Database initialization error: {e}")
        return None

def save_to_db(tree):
    try:
        tree.write(DATABASE)
    except IOError as e:
        print(f"Error saving to database: {e}")

def add_note(topic, note_name, text):
    try:
        tree = init_db()
        root = tree.getroot()
        timestamp = time.strftime("%m/%d/%y - %H:%M:%S")

        for elem in root.findall("topic"):
            if elem.get("name") == topic:
                note = ET.SubElement(elem, "note", name=note_name)
                ET.SubElement(note, "text").text = text
                ET.SubElement(note, "timestamp").text = timestamp
                save_to_db(tree)
                return "Note added"

        new_topic = ET.SubElement(root, "topic", name=topic)
        note = ET.SubElement(new_topic, "note", name=note_name)
        ET.SubElement(note, "text").text = text
        ET.SubElement(note, "timestamp").text = timestamp
        save_to_db(tree)
        return "New topic created and note added"
    except Exception as e:
        print(f"Error in add_note: {e}")
        return "Server error while adding note"

def get_notes(topic):
    try:
        tree = init_db()
        root = tree.getroot()
        for elem in root.findall("topic"):
            if elem.get("name") == topic:
                return [{"name": note.get("name"), 
                         "text": note.find("text").text, 
                         "timestamp": note.find("timestamp").text} 
                        for note in elem.findall("note")]
        return []
    except Exception as e:
        print(f"Error in get_notes: {e}")
        return "Server error while fetching notes"

def run_server():
    server = ThreadedXMLRPCServer(("localhost", PORT), allow_none=True)
    server.register_function(add_note, "add_note")
    server.register_function(get_notes, "get_notes")
    print(f"Server running on port {PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
