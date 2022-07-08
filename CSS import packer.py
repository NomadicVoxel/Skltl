About = \
	"CSS import packer \n  " + \
	"This script assembles CSS that has been sharded with imports. \n  " + \
	"Note that for now it is only meant for relative paths, remote paths are a work in progress. \n"

DefaultInput = "Skltl.css"
DefaultOutput = "Skltl.OneFile.css"

import os

def TrimImportPath(x):
	# "@import url('foo')" -> "foo"
	return x.strip().removeprefix("@import").strip().removeprefix("url(").removesuffix(");").strip(' "\'')

def JoinPath(Path, Line):
	x = os.path.join( os.path.dirname(Path), Line)
	return x

def ProcessFile(Path):
	NewFile = ""
	with open(Path) as File:
		for Line in File:
			if(Line.startswith("@import")):
				imported = JoinPath(Path,TrimImportPath(Line))
				NewFile += ("/* Importing " + TrimImportPath(Line) + "*/\n")
				NewFile += ProcessFile(imported)
			else:
				NewFile += Line
		NewFile += ("\n/* End of file " + os.path.basename(Path) + "*/\n") 
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
	with open(PathOut, 'w') as SaveFile: SaveFile.write(NewFile)

Main()