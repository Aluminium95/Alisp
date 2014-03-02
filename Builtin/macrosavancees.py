# macrosavancees.py
#
# Lopez Aliaume
#
# Contient les macros 
# plus avancées du langage

# TODO: Créer un matcheur déstructurant ! (type ocaml/haskell)
def match (contexte, variable, dico):
	# 
	# ---- Faire un match structurel !
	# 		: permettre des variables 	
	# 		: permettre des 
	variable = variable.eval (contexte)
	
	# une putain de grosse fonction qui fait un match sur des valeurs 
	for i in dico.dico: # pour chaque clef on teste si on matche 
		if variable.__eq__ (i):
			return dico.dico[i]
	return cel.Erreur (cel.Atome ("NoMatch"), variable)
	
	
# Codegen et codegeneval sont plutôt 
# pénibles à utiliser pour le moment dans 
# du code alisp ... peut-être trouver un 
# moyen plus simple de le faire ?
def codegen (contexte, expr):
	""" Crée du code à partir d'une 
		expression ... c'est à dire
		retourne la même expression 
		mais en remplaçant les 
		termes qui commencent par 
		un (replace)
		
		euh ... ce code plante quand utilisé 
		de manière récursive ... 
	"""
	if isinstance (expr, cel.Liste):
		if len (expr.liste) > 0:
			if expr.liste[0] == cel.Variable ("@"):
				if len (expr.liste) > 2:
					l = [ i.eval (contexte) for i in expr.liste]
					return cel.Liste (l)
				else:
					return expr.liste[1].eval (contexte)
			else:
				l = [ codegen (contexte, e) for e in expr.liste ]
				return cel.Liste (l)
		else:
			return cel.Liste ([])
	else:
		return expr
		

def codegeneval (contexte, expr):
	a = codegen (contexte, expr)
	return vareval (contexte, a)

