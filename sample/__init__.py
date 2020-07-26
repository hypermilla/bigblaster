import os 
from Bio.Blast.Applications import *
from tkinter import *
from tkinter import filedialog
from tkinter import ttk 

# Setting up folder structure: Current path, output folder, data folder
folder = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(folder, 'output')
output_file = os.path.join(folder, output_folder, 'big_blaster.xls')

# Initialize variables 
db_file = ''
query_file = ''
extensions = ['.xls', '.xml']
outputFmtOptions = [
	'0 = pairwise',
	'1 = query-anchored showing identities',
	'2 = query-anchored no identities',
	'3 = flat query-anchored, show identities',
	'4 = flat query-anchored, no identities',
	'5 = XML Blast output',
	'6 = tabular',
	'7 = tabular with comment lines',
	'8 = Text ASN.1',
	'9 = Binary ASN.1',
	'10 = Comma-separated values',
	'11 = BLAST archive format (ASN.1)',
	'12 = Seqalign (JSON)',
	'13 = Multiple-file BLAST JSON',
	'14 = Multiple-file BLAST XML2',
	'15 = Single-file BLAST JSON',
	'16 = Single-file BLAST XML2',
	'17 = Sequence Alignment/Map (SAM)',
	'18 = Organism Report']


# Functions to create file paths
def setQueryFile():
	global query_file
	query_file = filedialog.askopenfilename(
		initialdir=folder, 
		title='Select your Query File in FASTA format',
		filetypes=(('FASTA files', '*.fasta'),))
	msg_data_file.configure(text = query_file)
	if db_file != '':
		button_blast.configure(state = NORMAL)

def setOutputFolder():
	global output_folder
	output_folder = filedialog.askdirectory(
		initialdir=folder,
		title='Select a directory to save your database and results')
	print('Selected output folder: ' + output_folder)
	msg_output_folder.configure(text = 'Selected: ' + output_folder)

# BLAST functions 
def makeBlastDB():
	global db_file 
	db_file = filedialog.askopenfilename(
		initialdir=folder, 
		title='Select your Database File in FASTA format',
		filetypes=(('FASTA files', '*.fasta'),('FASTA files', '*.fa')))
	print('Selected DB File: ' + db_file)
	msg_make_db.configure(text = 'Selected: ' + db_file)
	button_make_db.configure(state = NORMAL)
	print('Making Blast DB: ' + db_file)

	db = NcbimakeblastdbCommandline(input_file=db_file, dbtype='nucl')
	database, database_err = db() 
	print('Err: ' + database_err)

	if database_err == '':
		msg_make_db.configure(text = 'Database created successfully!')
	else:
		msg_make_db.configure(text = database_err)
	if query_file : 
		button_blast.configure(state = NORMAL)

def blast(query_file, db_file, outputFmt, file, extension):
	outfmt = outputFmtOptions.index(outputFmt)
	print(outfmt)
	filename = file + extension
	global output_file
	output_file = os.path.join(output_folder, filename)
	blast = NcbiblastnCommandline(query=query_file, db=db_file, outfmt=outfmt, out=output_file)
	blast_output, blast_err = blast()
	if blast_err == '':
		msg_blast.configure(text = 'BLASTED!')


# Creating UI Window
root = Tk() 
root.geometry("460x900")
root.title('BIG BLASTER')

headerFrame = Frame(root, height=200, width=480)
bg_path = os.path.join(folder, 'blaster_header.png')
header_bg = PhotoImage(file = bg_path)
header = Label(headerFrame, image=header_bg)
header.place(x=0, y=0, relwidth=1, relheight=1)
headerFrame.pack()

frame = Frame(root)
frame.pack(padx=80, pady=10) 


# Make Blast DB from file 
label_make_db = Label(frame, text='Make a Blast Database', font='Arial, 18')
label_make_db.pack(padx= 3, pady = 8, fill=X)
button_make_db = Button(frame, 
	text='Create your Blast DB from file',
	command=lambda :makeBlastDB())
button_make_db.pack(padx= 3, pady = 3, fill=X)
msg_make_db = Label(frame, text='   ')
msg_make_db.pack(padx= 3, pady = 3, fill=X)


# Select Query file 
label_data_file = Label(frame, text='Select a Query file', font='Arial, 18')
label_data_file.pack(padx= 3, pady = 8, fill=X)
button_data_file = Button(frame, text='Add Data file to be used as Query', command=setQueryFile)
button_data_file.pack(padx= 3, pady = 3, fill=X)
msg_data_file = Label(frame, text='   ')
msg_data_file.pack(padx= 3, pady = 3, fill=X)


# Select output options
label_output_file = Label(frame, text='Define output options', font='Arial, 18')
label_output_file.pack(padx= 3, pady = 8, fill=X)

label_output_folder = Label(frame, text='Select folder to save results', font='Arial, 14')
label_output_folder.pack(padx = 3, pady = 3, fill = X)
button_output_folder = Button(frame, text='Add output folder', command=setOutputFolder)
button_output_folder.pack(padx = 3, pady = 3, fill=X)
msg_output_folder = Label(frame, text='  ')
msg_output_folder.pack(padx=3, pady=3, fill=X)


label_output_file = Label(frame, text='Define an output file name and extesion', font='Arial, 14')
label_output_file.pack(padx = 3, pady = 3, fill = X)

# Separate frame for output filename and extension, for formatting
outputFileFrame = Frame(frame)
outputFileFrame.pack(padx=20)

entry_output = Entry(outputFileFrame)
entry_output.insert(0, 'big_blast_output')
entry_output.pack(padx= 3, pady = 3, side=LEFT)

extComboBox = ttk.Combobox(outputFileFrame, values = extensions, state='readonly')
extComboBox.set(extensions[0])
extComboBox.pack(padx= 3, pady = 2, side=LEFT)

msg_output_file = Label(frame, text='  ')
msg_output_file.pack(padx= 3, pady = 2, fill = X)

# Define output formatting based on Blast's options 
label_output_file = Label(frame, text='Select an output format. Default is 6.', font='Arial, 14')
label_output_file.pack(padx = 3, pady = 3, fill = X)

outputFmt = ttk.Combobox(frame, values = outputFmtOptions, state='readonly')
outputFmt.set(outputFmtOptions[6])
outputFmt.pack(padx = 3, pady = 2, fill = X)

# Perform BLAST 
label_blast = Label(frame, text='Blast Query against Database', font='Arial, 18')
label_blast.pack(padx= 3, pady = 14, fill = X)
button_blast = Button(frame, 
	text='BLAST IT',
	height = '3',
	command=lambda :blast(query_file, db_file, outputFmt.get(), entry_output.get(), extComboBox.get()),
	state=DISABLED)
button_blast.pack(padx= 3, pady = 3, fill = X)
msg_blast = Label(frame, text='Create a database and select a query')
msg_blast.pack(padx= 3, pady = 6)


root.mainloop()