#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Utility to convert PDF spreads into pages
"""

#PyPDF2 https://github.com/mstamy2/PyPDF2
import PyPDF2, os, tkFileDialog
from Tkinter import *

class Application(Frame):
    #initialize menu and window settings
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.pack(fill=BOTH, expand=1)

        self.parent.title("PDF Spread Splitter")

        #menu
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu.add_command(label="Open", command=self.file_select)
        filemenu.add_command(label="Quit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        #app window
        width = 400
        height = 250

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - width)/2
        y = (sh - height)/2

        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))

        Button(self, text="Load a file", command=self.file_select).pack()

        self.frame_current_loaded_file_info = Frame(self)
        self.frame_current_loaded_file_info.pack()

        self.current_loaded_filename = StringVar()
        Label(self.frame_current_loaded_file_info, width=250, textvariable=self.current_loaded_filename).pack()

        self.saveas = "_pages"
        
        Button(self, text="Split", command=self.split).pack()

        self.progress = StringVar()
        self.progress_label = Label(self, textvariable=self.progress)
        self.progress_label.pack()

    #select input file
    def file_select(self):
        file_types = [('PDF Files', '*.pdf'), ('All Files', '*')]
        dialog = tkFileDialog.Open(self, filetypes=file_types)
        selected_file = dialog.show()
        if selected_file != "":
            self.inputStream = file(selected_file, "rb")
            self.inpdf = PyPDF2.PdfFileReader(self.inputStream)
            self.inputStream2 = file(selected_file, "rb")
            self.inpdf2 = PyPDF2.PdfFileReader(self.inputStream2)
            outfile_root, outfile_ext = os.path.splitext(selected_file)
            self.outfile = outfile_root + self.saveas + outfile_ext
            self.current_loaded_filename.set(os.path.basename(selected_file) + " --> " + os.path.basename(self.outfile))

    #split input file into pages
    def split(self):
        outpdf = PyPDF2.PdfFileWriter()
        #get corner locations
        llx,lly = self.inpdf.getPage(0).cropBox.lowerLeft
        urx,ury = self.inpdf.getPage(0).cropBox.upperRight
        for i in xrange(self.inpdf.getNumPages()):
            #left side
            self.inpdf.getPage(i).cropBox.lowerLeft = (llx,lly)
            self.inpdf.getPage(i).cropBox.upperRight = ((llx+urx)/2,ury)
            outpdf.addPage(self.inpdf.getPage(i))
            #right side
            self.inpdf2.getPage(i).cropBox.lowerLeft = ((llx+urx)/2,lly)
            self.inpdf2.getPage(i).cropBox.upperRight = (urx,ury)
            outpdf.addPage(self.inpdf2.getPage(i))
        #save output
        self.progress.set("saving...")
        outputStream = file(self.outfile, "wb")
        outpdf.write(outputStream)
        self.inputStream.close()
        self.inputStream2.close()
        outputStream.close()
        self.progress.set("done")

    #close
    def on_exit(self):
        self.quit()

def main():
    root = Tk()
    app = Application(root)

    root.mainloop()

if __name__ == '__main__':
    main()
