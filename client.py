import xmlrpc.client
PORT = 1000
server_url = f"http://localhost:{PORT}"
client = xmlrpc.client.ServerProxy(server_url)

while True:
    try:
        print("1. Add Note")
        print("2. Get Notes")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            topic = input("Enter topic: ")
            note_name = input("Enter note name: ")
            text = input("Enter note text: ")
            print(client.add_note(topic, note_name, text))
        elif choice == "2":
            topic = input("Enter topic: ")
            notes = client.get_notes(topic)
            if notes:
                print("Notes:")
                for note in notes:
                    print(f"- {note['name']}: {note['text']} ({note['timestamp']})")
            else:
                print("No notes found for this topic.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")
    except Exception as e:
        print(f"An error occurred: {e}")