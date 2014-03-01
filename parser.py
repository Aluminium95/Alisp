#-*- coding: utf-8 -*-
# parser.py
#
# Aliaume Lopez
#
# Utilise les tokens
# pour créer un AST
# à partir les éléments de Cellule

import tokenizer as tok
import cellule as cel

# TODO: récupérer les macros
# 	puis les développer dans 
#	l'arbre de syntaxe abstrait
#	avant l'exécution du code !
#
# ---- Important ---- 
#
# 	Idée : créer un fichier entre-temps 
# 			qui va modifier l'arbre 
#			optimisations de contexte 
#			et modification des macros !


# Parser : 
# transforme les tokens du tokenizer 
# en un arbre de syntaxe abstrait 
# avec la vraie nature des objets !
# C'est à dire que ce que retourne 
# le parser est déjà du code alisp
# (juste pas interprété pour le moment)
#
#
# C'est juste un travail de conversion 

class Parser:
	def __init__ (self):
		pass
		
	def parse (self, token):
		if isinstance (token, list): # si on a une liste de tokens 
			l = [cel.Variable ("body")] # body signifie qu'on a plusieurs éléments 
			# et que seul le dernier donnera sa valeur à l'expression 
			for i in token:
				l.append (self.parse (i))
			return cel.Liste (l) # On crée une véritable Liste (cellule) 
		elif isinstance (token, tok.String):
			return cel.String (token.valeur)
		elif isinstance (token, tok.Nombre):
			return cel.Nombre (token.val)
		elif isinstance (token, tok.Atome):
			return cel.Atome (token.val)
		elif isinstance (token, tok.Liste):
			l = []
			for i in token.liste:
				l.append (self.parse (i))
			return cel.Liste (l)
		elif isinstance (token, tok.Dict):
			l = []
			for i in token.liste:
				l.append (self.parse (i))
			return cel.Dico (l)
		elif isinstance (token, str): # symbole
			# alphanum plus tard ici TODO
			return cel.Variable (token)
		else:
			raise ValueError ("Token inconnu")

