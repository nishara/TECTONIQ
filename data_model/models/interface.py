__author__ = 'Nishara'


from Tkinter import *


class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Create the Label
        self.search_query = Label(self, text = "Enter your search query")
        self.search_query.grid(row=0, column=0, columnspan = 2, sticky = W)

        # Create the Entry field
        self.query = Entry(self)
        self.query.grid(row=1, column=1, sticky =W)

        # Add Submit Button
        self.button1 = Button(self, text ="Submit", command = self.get_query)
        self.button1.grid(row=2, column=0, columnspan = 2, sticky = W)

        # Add a text field to return a message
        self.text = Text(self, width =35, height =5, wrap = WORD)
        self.text.grid(row=3, column=0, columnspan = 2, sticky = W)

    def get_query(self):
        content = self.query.get()
        message = "Your query has been submitted"
        self.text.insert(0.0, message)
        print content

if __name__ == '__main__':
        root = Tk()
        root.title("Tectonique User Interface")
        Application(root)
        root.mainloop()