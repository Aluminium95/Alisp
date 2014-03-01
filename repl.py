#-*- coding: utf-8 -*-
# repl.py
#
# Aliaume Lopez
#
# Fait une interaction avec l'utilisateur
# c'est trop cool nan ?
# 
# On crée un contexte toplevel 
# avec toutes les fonctions de base
# chargées, et on lance les commandes dedans 
#

try:
	import readline # si on est sous linux ... (permet l'édition)
except:
	print ("Readline n'est pas présent ... le prompt sera pourri")
	
import tokenizer as tok
import parser as par
import executeur as exe
import cellule as cel


contexte = cel.Contexte ()

# Ajoute les built-ins !
exe.addBuiltInFuncs (contexte, exe.built_in_funcs)
exe.addBuiltInMacros (contexte, exe.built_in_macros)
	
def parentmatch (text):
	""" Une fonction qui vérifie que l'on 
		a bien le bon nombre de parenthèses 
		(ie : la syntaxe est bonne)
	"""
	par = 0
	acc = 0
	
	for i in text:
		if i == "(":
			par += 1
		elif i == ")":
			par -= 1
		elif i == "{":
			acc += 1
		elif i == "}":
			acc -= 1
	
	if par == 0 and acc == 0:
		return True
	else:
		return False

t = tok.Tokenizer ()
p = par.Parser ()
buf = "" # le buffer ... 
prompt = "> " # le prompt (ce qui s'affiche devant la saisie utilisateur)

while True:
	buf += input (prompt)
	if parentmatch (buf): # si on peut dire que cela est susceptible de tourner
		b = t.tokenize (buf)
		c = p.parse (b)
		print (" --- # {}".format (c))
		d = exe.eval (c, contexte)
		print ("{}".format (d))
		buf = ""
		prompt = "> "
	else: # sinon on attend les parenthèses supplémentaires 
		prompt = "... > "
		
		
