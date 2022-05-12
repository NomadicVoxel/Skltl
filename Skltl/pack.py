About = "/* CSS Assembler \n  " + \
	"This script assembles CSS that has been sharded with imports. \n  " + \
	"or it would if it were finished, anyway. \n  " + \
	"Note that relative paths are a work in progress. \n  */"

DefaultPath = "Skltl.css"

import os

def TrimImportPath(x):
	# "@import url('foo')" -> "foo"
	return x.removeprefix('@import').strip().removeprefix("url(").removesuffix(")").strip()[0:-2]

def JoinPath(Path, Line):
	x = os.path.join( os.path.dirname(Path), Line)
	return x

def ProcessFile(Path):
	NewFile = ""
	with open(Path) as File:
		for Line in File:
			if(Line.startswith("@import")):
				imported = JoinPath(Path,TrimImportPath(Line))
				NewFile += ("/* Importing " + imported + "*/\n")
				NewFile += ProcessFile(imported)
			else:
				NewFile += Line
		NewFile += ("\n/* End of file " + Path + "*/\n") 
	return NewFile

def Main():
	print(About)
	# Path = input("Enter path to the root file of CSS. \n(Blank defaults to "+DefaultPath+") \n>")
	print("Starting with " + os.path.join(os.path.dirname(__file__),DefaultPath))
	Path = os.path.join(os.path.dirname(__file__),DefaultPath)
	# if(Path == ""): 
		# Path = DefaultPath
	NewFile =  "/* Skltl is a modular CSS framework, with an objective of using as few classes and wrappers.\n "
	NewFile += "In other words, to use semantic HTML instead, and to make nearly any HTML that *wasn't* designed for it half decent. \n"
	NewFile += "The original makes extensive use of imports to make it modular. \n"
	NewFile += "Source code = https://github.com/NomadicVoxel/Skltl*/"
	NewFile += ProcessFile(Path)
	print(NewFile)
	with open("Skltl.OneFile.css", 'w') as SaveFile: SaveFile.write(NewFile)
Main()