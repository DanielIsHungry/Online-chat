import ttkbootstrap as ttk
import firebase_admin
from firebase_admin import credentials, db
from tkinter.simpledialog import askstring



class Application:
    CRED = 'your credentials here' # Insert your firebase credentials here
    firebase_admin.initialize_app(CRED, {
        'databaseURL': 'your-app-here' # Insert your application here
    })
    print('started firebase')

    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x400')

        self.label_frame = ttk.Frame(self.root, padding=10)
        self.label_frame.pack(fill="x")

        self.username = ''

        ttk.Label(
            self.label_frame,
            text="Online chat",
            font=('Bahnschrift Condensed', 36, 'bold')
        ).pack(expand=True, padx=5, pady=10)

        ttk.Button(
            self.root,
            text='Get started',
            width=20,
            command=self.start
        ).pack(side="left", expand=True, padx=100, pady=10, fill='x')

    def start(self):
        self.username = askstring('Username', 'Just before you get started, what would you like to call yourself?')
        for child in self.root.winfo_children():
            child.destroy()

        self.chat = ttk.Treeview(self.root, columns=('Name', 'Message'), show="headings")
        self.chat.pack(fill="both", expand=True, padx=10, pady=10)
        self.chat.heading("Name", text="Name")
        self.chat.heading("Message", text="Message")

        self.msg_entry = ttk.Entry(self.root)
        self.msg_entry.pack(fill='x', padx=10, pady=5)
        self.msg_entry.bind('<Return>', self.send_message)

        db.reference('messages').listen(self.on_message)

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        if msg.strip():
            data = {
                'name': self.username,
                'message': msg
            }
            db.reference('messages').push(data)
            self.msg_entry.delete(0, 'end')

    def on_message(self, event):
        if not event.data:
            return

        if event.event_type == 'put' and event.path == '/':
            self.chat.delete(*self.chat.get_children())
            if isinstance(event.data, dict):
                for key, val in event.data.items():
                    if isinstance(val, dict) and 'name' in val and 'message' in val:
                        self.chat.insert('', 'end', values=(val['name'], val['message']))
        elif event.event_type == 'put':
            val = event.data
            if isinstance(val, dict) and 'name' in val and 'message' in val:
                self.chat.insert('', 'end', values=(val['name'], val['message']))


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = Application(root)
    root.mainloop()
