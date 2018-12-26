import os

files = os.listdir("data/")

for file in files:
	print(file)
	os.system("xhtml2pdf data/" + file + "/data.html")