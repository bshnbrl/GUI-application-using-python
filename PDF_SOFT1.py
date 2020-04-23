import os
os.chdir('D:')
os.getcwd()

#----------PDF software exe development-------------------
import PyPDF2; print("PyPDF2 version---",PyPDF2.__version__)
from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from collections import defaultdict
#1) Functions for execution of operation
def split(path, name_of_split):
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output = f'{name_of_split}{page}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
   
def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
    txt = f"""Information about {pdf_path}:
    Author: {information.author}      Creator: {information.creator}
    Producer: {information.producer}  Subject: {information.subject}
    Title: {information.title}        Number of pages: {number_of_pages}"""
    return txt

def add_encryption(input_pdf, output_pdf, password):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_pdf)
    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))
        pdf_writer.encrypt(user_pwd=password, owner_pwd=None,use_128bit=True)
    with open(output_pdf, 'wb') as fh:
        pdf_writer.write(fh)
    txt_edit.insert(tk.END, f'{os.path.basename(f_p)}{"--file encrpytion complete"}')
    txt_edit.insert(tk.END, "\n----------------------\n")

def mrg_pdfs(paths, output):
    print(paths)
    pdf_writer = PdfFileWriter()
    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))
    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)
    txt_edit.insert(tk.END, f'{val1}{"--Merged file created"}')
    txt_edit.insert(tk.END, "\n----------------------\n")

#2) Functions for execution of button click
def info_pdf():
    filepath = askopenfilename(filetypes=[("pdf", "*.pdf"), ("All Files", "*.*")])
    if not filepath:#check to see if the user closes the dialog box or clicks the Cancel button.
        return
    txt_edit.insert(tk.END, extract_information(filepath))
    txt_edit.insert(tk.END, "\n----------------------\n")

def merge_pdf():
    new_win1 = tk.Toplevel(window, width=30, height=30)
    new_win1.title("pdf merging")
    new_dict = defaultdict()
    def fp2(brw,i):
        global f_p, pdf_list
        f_p = askopenfilename(filetypes=[("pdf", "*.pdf"), ("All Files", "*.*")])
        if not f_p:#check to see if the user closes the dialog box or clicks the Cancel button.
            return
        brw.delete(1.0, tk.END)
        brw.insert(tk.END,f_p)
        #new_dict = dict.fromkeys(range(5),)
        new_dict[i] = os.path.basename(f_p)
        pdf_list = list(new_dict.values())
        #f'{"lst_"}{i}' #use iterate to get all 5 element separate then generate list of it then pass it to fun
        print(i,pdf_list)
        return pdf_list
    brw_pdf1 = tk.Text(new_win1,height=1,width=50)
    brw_pdf1.grid(row=0, column=1, sticky="ew")
    brw_pdf2 = tk.Text(new_win1,height=1,width=50)
    brw_pdf2.grid(row=1, column=1, sticky="ew")
    brw_pdf3 = tk.Text(new_win1,height=1,width=50)
    brw_pdf3.grid(row=2, column=1, sticky="ew")
    brw_pdf4 = tk.Text(new_win1,height=1,width=50)
    brw_pdf4.grid(row=3, column=1, sticky="ew")
    brw_pdf5 = tk.Text(new_win1,height=1,width=50)
    brw_pdf5.grid(row=4, column=1, sticky="ew")
    e2 = tk.Entry(new_win1,width=50) #enter merged pdf name with .pdf
    e2.grid(row=5, column=1, sticky="ew")
    
    def f_mrg():
        global val1
        val1 = e2.get()
        if val1 is "":
            tk.Label(new_win1, text="please enter output pdf name").grid(row=6,column=1)
            return
        else:
            print(pdf_list)
            mrg_pdfs(pdf_list, val1)
        new_win1.destroy()
    tk.Button(new_win1, text = "Browse_pdf1",command=lambda:fp2(brw_pdf1,0)).grid(row=0, column=0, sticky="ew")
    tk.Button(new_win1, text = "Browse_pdf2",command=lambda:fp2(brw_pdf2,1)).grid(row=1, column=0, sticky="ew")
    tk.Button(new_win1, text = "Browse_pdf3",command=lambda:fp2(brw_pdf3,2)).grid(row=2, column=0, sticky="ew")
    tk.Button(new_win1, text = "Browse_pdf4",command=lambda:fp2(brw_pdf4,3)).grid(row=3, column=0, sticky="ew")
    tk.Button(new_win1, text = "Browse_pdf5",command=lambda:fp2(brw_pdf5,4)).grid(row=4, column=0, sticky="ew")
    tk.Label(new_win1, text="Name of Merged pdf:").grid(row=5,column=0) #name of merged pdf file
    tk.Button(new_win1, text = "Merge pdfs",command=f_mrg).grid(row=6, sticky="ew")

def split_pdf():
    filepath = askopenfilename(filetypes=[("pdf", "*.pdf"), ("All Files", "*.*")])
    if not filepath:#check to see if the user closes the dialog box or clicks the Cancel button.
        return
    split(filepath, 'page_')
    txt_edit.insert(tk.END, filepath)
    txt_edit.insert(tk.END, " splitting completed\n----------------------\n")
    
def encrpyt_pdf():
    new_win = tk.Toplevel(window, width=30, height=30)
    new_win.title("encrpyt page")
    def fp1():
        global f_p
        f_p = askopenfilename(filetypes=[("pdf", "*.pdf"), ("All Files", "*.*")])
        if not f_p:#check to see if the user closes the dialog box or clicks the Cancel button.
            return
        txt_brw.insert(tk.END,f_p)#txt_edit.delete(1.0, tk.END)
        return f_p
    btn_brw = tk.Button(new_win, text = "Browse",command=fp1)
    btn_brw.grid(row=0, column=0, sticky="ew")
    txt_brw = tk.Text(new_win,height=1,width=50)
    txt_brw.grid(row=0, column=1, sticky="ew")
    tk.Label(new_win, text='Password').grid(row=1,column=0)
    e1 = tk.Entry(new_win,width=50,show='*')
    e1.grid(row=1, column=1, sticky="ew")
    tk.Label(new_win, text='*remember your password ').grid(row=1,column=2)
    tk.Label(new_win, text='*select your pdf ').grid(row=0,column=2)
    def f_enc():
        pwd = e1.get()
        add_encryption(input_pdf=f_p, output_pdf=f'{os.path.splitext(os.path.basename(f_p))[0]}{"_encrpyted"}.pdf', password=pwd)
        new_win.destroy()
    tk.Button(new_win, text = "Encrpyt",command=f_enc).grid(row=2, sticky="ew")
#3) Main program to run 
window = tk.Tk()
window.title("PDF-software")
window.rowconfigure(0, minsize=400, weight=1)
window.columnconfigure(1, minsize=400, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

tk.Button(fr_buttons, text="Info", command = info_pdf).grid(row=0, column=0, sticky="ew", padx=5, pady=5) #position of button in frame
tk.Button(fr_buttons, text="Merge", command=merge_pdf).grid(row=1, column=0, sticky="ew", padx=5, pady=5) #position of button in frame
tk.Button(fr_buttons, text="Split", command=split_pdf).grid(row=2, column=0, sticky="ew", padx=5, pady=5) #position of button in frame
tk.Button(fr_buttons, text="Encrpyt", command=encrpyt_pdf).grid(row=3, column=0, sticky="ew", padx=5, pady=5) #position of button in frame
tk.Button(fr_buttons, text="Close",width=30, command=window.destroy).grid(row=4, column=0, sticky="ew", padx=5, pady=5) #position of button in frame

fr_buttons.grid(row=0, column=0, sticky="ns") #position of buttons
txt_edit.grid(row=0, column=1, sticky="nsew") #position of text area

window.mainloop()
