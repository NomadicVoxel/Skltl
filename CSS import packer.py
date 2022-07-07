About = \
	"CSS import packer \n  " + \
	"This script assembles CSS that has been sharded with imports. \n  " + \
	"Note that for now it is only meant for relative paths, remote paths are a work in progress. \n"

import os

DefaultInput = "Skltl.css"
DefaultOutput = "Skltl.OneFile.css"

def TrimImportPath(x):
	# "@import url('foo')" -> "foo"
	return x.removeprefix('@import').strip().removeprefix("url(").removesuffix(")").strip(' "\'')[0:-2]

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
	PathIn = input("Enter path to the root file of CSS. \n(Blank defaults to "+DefaultInput+") \n>>>")
	if(PathIn == ""): 
		PathIn = os.path.join(os.path.dirname(__file__),DefaultInput)
	PathOut = input("Enter output filename. \n(Blank defaults to "+DefaultOutput+") \n>>>")
	if(PathOut == ""):
		PathOut = os.path.join(os.path.dirname(__file__),DefaultOutput)
	NewFile = "/* This CSS was originally composed of several files broken into imports. Here it is compiled into one file instead. */"
	NewFile += ProcessFile(PathIn)
	print(NewFile)
	with open("Skltl.OneFile.css", 'w') as SaveFile: SaveFile.write(NewFile)

Main()