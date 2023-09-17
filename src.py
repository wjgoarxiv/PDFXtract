import pdfplumber
import tkinter as tk
from tkinter import filedialog, Text, ttk
import markdown
import webbrowser
import tempfile
import os
import pyperclip
import platform

if platform.system() == 'Windows':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

# Global variable to hold the file path of the selected PDF
selected_pdf_file = ""
# Global variable to hold the text content per page
text_content_per_page = {}

def load_pdf_file():
    global selected_pdf_file    
    # Open file dialog
    selected_pdf_file = filedialog.askopenfilename()
    # Check if the selected file is a PDF
    if not selected_pdf_file.lower().endswith('.pdf'):
        error_label.config(text="⚠️  ERROR: Please select a PDF file.")
        return
    else:
        error_label.config(text="INFO: PDF file loaded. Click 'Convert!' to proceed.")
        print("INFO: PDF file loaded.")

def extract_and_display_pdf():
    global text_content_per_page
    # Clear existing content in the Text widget
    text_widget.delete('1.0', tk.END)
    
    if not selected_pdf_file:
        error_label.config(text="⚠️  ERROR: No PDF file loaded.")
        return
    
    text_content_per_page.clear()
    
    # Extract text from each page and store it in the dictionary
    with pdfplumber.open(selected_pdf_file) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            text_content_per_page[i + 1] = text  # Page numbering starts from 1

    # Sort the dictionary by page number
    sorted_text_content = {k: text_content_per_page[k] for k in sorted(text_content_per_page)}
    
    # Display the sorted text content in Markdown format in the Text widget
    for page_num, text in sorted_text_content.items():
        markdown_text = f"### Text converted from page ({page_num} / {total_pages})\n\n{text}\n\n---\n"
        text_widget.insert(tk.END, markdown_text)

    error_label.config(text="INFO: PDF file successfully converted!")
    print("INFO: PDF file successfully converted!")

def copy_to_clipboard():
    clipboard_text = text_widget.get("1.0", tk.END)
    pyperclip.copy(clipboard_text)
    error_label.config(text="INFO: Text copied to clipboard.")
    print("INFO: Text copied to clipboard.")

def copy_specific_page():
    try:
        page_num = int(page_entry.get())
        page_text = text_content_per_page.get(page_num, "Page not found.")
        pyperclip.copy(page_text)
        error_label.config(text="INFO: Specific page copied to clipboard.")
        print("INFO: Specific page copied to clipboard.")
    except ValueError:
        error_label.config(text="⚠️  ERROR: Invalid page number.")

def preview_markdown():
    md_text = text_widget.get("1.0", tk.END)
    html_text = markdown.markdown(md_text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp:
        temp.write(html_text.encode("utf-8"))

    try: 
        # Try to open the temporary HTML file in the default web browser
        webbrowser.open_new_tab(f"file://{temp.name}")
    except: 
        # Fallback method for Linux environments
        os.system(f"xdg-open {temp.name}")

    error_label.config(text="INFO: Markdown preview opened in browser.")
    print("INFO: Markdown preview opened in browser.")

def open_github(): 
    if platform.system() == "Windows":
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
        webbrowser.get('chrome').open_new_tab('https://github.com/wjgoarxiv')
    elif platform.system() == "Linux":
        webbrowser.get('xdg-open').open_new_tab('https://github.com/wjgoarxiv')
    else:  # macOS and others
        webbrowser.open_new_tab('https://github.com/wjgoarxiv')

def save_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"),
                                                        ("Markdown files", "*.md")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_widget.get("1.0", tk.END))
        error_label.config(text="INFO: File successfully saved.")
        print("INFO: File successfully saved.")

# Initialize Tkinter window here
root = tk.Tk()
root.title("PDFXtract")
root.geometry("800x1200")

# Add title and author label
title_label = ttk.Label(root, text="PDFXtract", font=("Arial", 26))
title_label.pack(pady=5)

# Add the version label
ver_label = ttk.Label(root, text="V1.0.0", font=("Arial", 14))
ver_label.pack(pady=2)

# Add the description belwo the title 
description_label = ttk.Label(root, text="Your simple PDF to TXT converter", font=("Arial", 14))
description_label.pack(pady=10)

# Add the miscellaneous label (author, etc.) 
misc_label = ttk.Label(root, text="Made by: @wjgoarxiv", font=("Arial", 12))
misc_label.pack(pady=5)

# Make a button for the author's GitHub page
github_button = ttk.Button(root, text="🖱️ Visit my GitHub profile!", command=open_github)
github_button.pack(pady=5)

# Separator
ttk.Separator(root, orient='horizontal').pack(fill='x', padx=5, pady=10)

# Create a button to open a PDF file
open_file_button = ttk.Button(root, text="📂 Open PDF File", command=load_pdf_file)
open_file_button.pack(pady=10)

# Create a button to trigger text extraction and display
convert_button = ttk.Button(root, text="👍 Convert!", command=extract_and_display_pdf)
convert_button.pack(pady=10)

# Separator
ttk.Separator(root, orient='horizontal').pack(fill='x', padx=5, pady=10)

# Create a button to copy text to clipboard
copy_button = ttk.Button(root, text="📋 Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=10)

# Add entry to specify a page number for copying
page_entry = ttk.Entry(root, width=5)
page_entry.pack(side="left", padx=5)

# Create a button to copy specific page to clipboard
copy_specific_page_button = ttk.Button(root, text="📋 Copy Specific Page", command=copy_specific_page)
copy_specific_page_button.pack(side="left", padx=5)

# Create a button for Markdown preview
preview_button = ttk.Button(root, text="🔍 Preview Markdown", command=preview_markdown)
preview_button.pack(pady=10)

# Create a button to save text to file
save_button = ttk.Button(root, text="💾 Save As", command=save_to_file)
save_button.pack(pady=10)

# Separator
ttk.Separator(root, orient='horizontal').pack(fill='x', padx=5, pady=10)

# Create a button to exit the application
exit_button = ttk.Button(root, text="🚪 Exit", command=root.quit)
exit_button.pack(pady=10)

# Create a label to display errors
error_label = ttk.Label(root, text="", foreground="red")
error_label.pack(pady=10)

# Create a Text widget to display the PDF text
text_widget = Text(root, wrap=tk.WORD, width=80, height=40)
text_widget.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()