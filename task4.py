#contact book 
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json

class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        self.contacts = []

        # Create and set up the main menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.main_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Main Menu", menu=self.main_menu)

        self.main_menu.add_command(label="View Contact List", command=self.view_contacts)
        self.main_menu.add_command(label="Add Contact", command=self.add_contact)
        self.main_menu.add_command(label="Search Contact", command=self.search_contact)
        self.main_menu.add_command(label="Update Contact", command=self.update_contact)
        self.main_menu.add_command(label="Delete Contact", command=self.delete_contact)
        self.main_menu.add_separator()
        self.main_menu.add_command(label="Sort Contacts by Name", command=lambda: self.sort_contacts('Name'))
        self.main_menu.add_command(label="Sort Contacts by Phone", command=lambda: self.sort_contacts('Phone'))
        self.main_menu.add_separator()
        self.main_menu.add_command(label="Save Contacts", command=self.save_contacts)
        self.main_menu.add_command(label="Load Contacts", command=self.load_contacts)
        self.main_menu.add_separator()
        self.main_menu.add_command(label="Exit", command=self.root.destroy)

        # Dashboard to display contact names
        self.dashboard_label = tk.Label(self.root, text="Contact Names:")
        self.dashboard_label.pack()

    def view_contacts(self):
        if not self.contacts:
            messagebox.showinfo("View Contacts", "No contacts available.")
        else:
            contact_list = "\n".join([f"{contact['Name']}: {', '.join(contact['Phone'])}" for contact in self.contacts])
            messagebox.showinfo("View Contacts", contact_list)

    def add_contact(self):
        contact_details = self.get_contact_details("Add Contact")
        if contact_details:
            self.contacts.append(contact_details)
            self.update_dashboard()
            messagebox.showinfo("Add Contact", "Contact added successfully.")

    def search_contact(self):
        search_term = simpledialog.askstring("Search Contact", "Enter name or phone number:")
        if search_term:
            results = [contact for contact in self.contacts if
                       search_term.lower() in contact['Name'].lower() or search_term in contact['Phone']]
            if results:
                result_str = "\n".join([f"{contact['Name']}: {', '.join(contact['Phone'])}" for contact in results])
                messagebox.showinfo("Search Results", result_str)
            else:
                messagebox.showinfo("Search Results", "No matching contacts found.")

    def update_contact(self):
        search_term = simpledialog.askstring("Update Contact", "Enter name or phone number of the contact to update:")
        if search_term:
            contact_to_update = next((contact for contact in self.contacts if
                                      search_term.lower() in contact['Name'].lower() or search_term in contact['Phone']),
                                     None)
            if contact_to_update:
                updated_details = self.get_contact_details("Update Contact", contact_to_update)
                if updated_details:
                    self.contacts.remove(contact_to_update)
                    self.contacts.append(updated_details)
                    self.update_dashboard()
                    messagebox.showinfo("Update Contact", "Contact updated successfully.")
            else:
                messagebox.showinfo("Update Contact", "Contact not found.")

    def delete_contact(self):
        search_term = simpledialog.askstring("Delete Contact", "Enter name or phone number of the contact to delete:")
        if search_term:
            contact_to_delete = next((contact for contact in self.contacts if
                                      search_term.lower() in contact['Name'].lower() or search_term in contact['Phone']),
                                     None)
            if contact_to_delete:
                self.contacts.remove(contact_to_delete)
                self.update_dashboard()
                messagebox.showinfo("Delete Contact", "Contact deleted successfully.")
            else:
                messagebox.showinfo("Delete Contact", "Contact not found.")

    def sort_contacts(self, key):
        self.contacts.sort(key=lambda x: x[key])
        self.update_dashboard()

    def get_contact_details(self, title, existing_contact=None):
        name = simpledialog.askstring(title, "Enter Name:", initialvalue=existing_contact['Name'] if existing_contact else '')
        phone = simpledialog.askstring(title, "Enter Phone Number (separate multiple numbers with commas):", initialvalue=','.join(existing_contact['Phone']) if existing_contact else '')
        email = simpledialog.askstring(title, "Enter Email:", initialvalue=existing_contact['Email'] if existing_contact else '')
        address = simpledialog.askstring(title, "Enter Address:", initialvalue=existing_contact['Address'] if existing_contact else '')

        if name and all(num.isdigit() and len(num) == 10 for num in phone.split(',')):
            return {'Name': name, 'Phone': phone.split(','), 'Email': email, 'Address': address}
        else:
            messagebox.showwarning("Invalid Input", "Please enter a valid name and valid 10-digit phone number(s).")
            return None


    def update_dashboard(self):
        names = [contact['Name'] for contact in self.contacts]
        self.dashboard_label.config(text=f"Contact Names: {', '.join(names)}")

    def save_contacts(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
            if file_path:
                with open(file_path, 'w') as file:
                    json.dump(self.contacts, file)
                messagebox.showinfo("Save Contacts", "Contacts saved successfully.")
        except Exception as e:
            messagebox.showerror("Save Contacts", f"Error saving contacts: {e}")

    def load_contacts(self):
        try:
            file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
            if file_path:
                with open(file_path, 'r') as file:
                    self.contacts = json.load(file)
                self.update_dashboard()
                messagebox.showinfo("Load Contacts", "Contacts loaded successfully.")
        except FileNotFoundError:
            messagebox.showinfo("Load Contacts", "No saved contacts found.")
        except Exception as e:
            messagebox.showerror("Load Contacts", f"Error loading contacts: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()
