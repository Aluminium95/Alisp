#-*- coding: utf-8 -*-
# cellule.py
#
# Aliaume Lopez 
#
# Les types de base 
# pour Alisp
#
# TODO:
# 	- Gérer les erreurs comme des exceptions 
# 		+ raise error (python s'en charge)
#		+ try/catch (python idem)
#		+ match error (super match !)
#
#
# Débuger le problème de récursion !
# on ne peut pas faire de la récursion non 
# terminale (et celle-ci n'est pas optimisée)
# (cf : comment optimiser la récursion terminale est 
# 	une question intéressante qui mérite une réponse !)
# PS1 : après quelques recherches, ce n'est pas la 
# 		récursion terminale qu'il faut optimiser 
# 		mais un appel fonctionnel terminal quelconque
# 		ce qui est déjà plus facile : et plus puissant !
#
# TODO:
# 	Ajouter le contexte comme une classe de Alisp !
# 	en effet l'utilisateur pourrait vouloir 
# 	conserver le contexte parent et le modifier ?!
#   
# TODO:
# 	Séparer les cellules en plusieurs fichiers dans un 
# 	seul dossier, avec chaque classe qui a un seul
# 	et unique fichier pour plus de lisibilité !

from contexte import Contexte


class Cellule:
	""" Type de base dans ALisp """
	def __hash__ (self):
		return str (self).__hash__ () 
	
	def __eq__ (self, other):
		""" Méthode très peu efficace ! """
		return str (self) == str (other)
		
	def egal (contexte, a, b):
		if a == b:
			return Atome ("true")
		else:
			return Atome ("false")
	
	
class Lambda (Cellule):
	""" Une fonction """
	def __init__ (self, ctx, args, corps):
		self.args = args
		self.corps = corps
		self.string = False
		# le dernier argument est une liste des arguments en trop ?
		self.infinite = False
		self.ctx = ctx # retenir le contexte de création ...

	def __str__ (self):
		if self.string == False:
			self.string = "<fonction {}>".format (str (self.args))
		return self.string

	def eval (self, contexte):
		return self
	
	def tp (contexte, variable):
		if isinstance (variable, Lambda):
			return Atome ("true")
		else:
			return Atome ("false")
	
	def run (self, contexte, arguments):
		""" Lance la macro """
		# Crée le contexte d'appel
		# fusionne le contexte de création 
		# et le contexte d'appel pour créer un nouveau
		# contexte

		# C'est ici qu'il faut regarder la récursion !
		# Le dernier appel à une fonction ne nécessite 
		# pas de redéfinir le contexte 
		arguments = [ i.eval (contexte) for i in arguments ]
		ctx = self.ctx.fusion (contexte) 
		
		i = 0 # Ajoute les variables au (nouveau) contexte
		while i < min (len (self.args.liste), len (arguments)):
			if self.infinite == True and i == len (self.args.liste):
				# passe la liste des arguments restants 
				ctx.set (self.args.liste[i], Liste (arguments[i:]))
			else:
				ctx.set (self.args.liste[i], arguments[i])
			i += 1
		return self.corps.eval (ctx) # euh, yep !
		
class BuiltInLambda (Lambda):
	def __init__ (self, fonction, nom):
		self.f = fonction
		self.nom  = nom 
	
	def __str__ (self):
		return "<built-in-function {}>".format (self.nom)
	
	def run (self, contexte, arguments):
		try:
			args = [ i.eval (contexte) for i in arguments ]
			return self.f (contexte, *args)
		except Erreur as e:
			return e
		except:
			return Erreur (Atome ("Built-In-Func-Error"), String ("Une erreur est survenue"))
		
	
class Macro (Cellule):
	""" Une macro ! """
	def __init__ (self, ctx, args, corps):
		self.args = args
		self.corps = corps
		self.ctx = ctx
		# le dernier argument sert de ramasse-miette ?
		self.infinite = False
	
	def __str__ (self):
		return "<macro {}>".format (str (self.args))
		
	def eval (self, contexte):
		return self # Une macro s'évalue à une macro
	
	def run (self, contexte, arguments):
		""" Lance la macro """
		# Crée le contexte d'appel
		# fusionne le contexte de création 
		# et le contexte d'appel pour créer un nouveau
		# contexte 
		ctx = self.ctx.fusion (contexte) 
		i = 0 # Ajoute les variables au (nouveau) contexte
		while i < len (self.args.liste):
			if self.infinite == True and i == len (self.args.liste):
				# passe la liste des arguments restants 
				ctx.set (self.args.liste[i], Liste (arguments[i:]))
			else:
				ctx.set (self.args.liste[i], arguments[i])
			i += 1
		return self.corps.eval (ctx) # euh, yep !

class BuiltInMacro (Macro):
	def __init__ (self, fonction, nom):
		self.f = fonction 
		self.nom = nom
	
	def __str__ (self):
		return "<built-in-macro {}>".format (self.nom)
	
	def run (self, contexte, arguments):
		# TODO: rendre les messages plus informatifs ... 
		try:
			return self.f (contexte, *(arguments))
		except Erreur as e:
			return e
		except:
			return Erreur (Atome ("Built-In-Macro-Error"), String ("Une erreur est survenue ..."))
		
		

class String (Cellule):
	""" Une chaine de caractères """
	def __init__ (self, valeur):
		self.valeur = valeur
	
	def __str__ (self):
		return "\"{}\"".format (self.valeur)

	def append (ctx, *chaines):
		l = []
		for i in chaines:
			l.append (i.valeur)
		return String ("".join (l))
	
	def eval (self, contexte):
		return self
	
	def tp (contexte, variable):
		if isinstance (variable, String):
			return Atome ("true")
		else:
			return Atome ("false")

class Nombre (Cellule):
	""" Un nombre """
	def __init__ (self, valeur, den=1):
		self.valeur = valeur
		self.den = den
		self.exact = False
		if valeur / den == int (valeur/den):
			self.den = 1
			self.valeur = valeur / den

		if self.den == int (self.den) and self.valeur == int (self.valeur):
			self.exact = True
	
	def __str__ (self):
		if self.den == 1:
			return "{}".format (self.valeur)
		else:
			return "{}/{}".format (self.valeur, self.den)
	
	def __eq__ (self, other):
		if isinstance (other, Nombre) and other.valeur == self.valeur and self.den == other.den:
			return True
		else:
			return False
	
	def eval (self, contexte):
		return self
	
	def inexact (contexte, elem):
		return Nombre (elem.valeur / elem.den)
	
	def plus (contexte, *args):
		s = 0
		p = 1
		for i in args:
			k = i.eval (contexte)
			if isinstance (k, Nombre):
				s = s * (k.den) + k.valeur * p # regarder s'il y a des erreurs
				p *= k.den 
			else:
				return Erreur (Atome ("InvalidArgument"), String ("{} n'est pas un nombre".format (k)))
		return Nombre (s,p)
	
	def moins (contexte, *args):
		f = args[0].eval (contexte)
		if not isinstance (f, Nombre):
			return Erreur (Atome ("InvalidArgument"), String ("{} n'est pas un nombre".format (s)))
		s = f.valeur 
		d = f.den
		for i in args[1:]:
			a = i.eval (contexte)
			if isinstance (a, Nombre):
				s = s * a.den - a.valeur * d
				d = d * a.den
			else:
				return Erreur (Atome ("InvalidArgument"), String ("{} n'est pas un nombre".format (s)))
		
		return Nombre (s,d)
	
	def mult (contexte, *args):
		s = 1
		d = 1
		for i in args:
			n = i.eval (contexte)
			s *= n.valeur
			d *= n.den
		return Nombre (s,d)
	
	def div (contexte, *args):
		f = args[0].eval (contexte)
		s = f.valeur
		d = f.den
		for i in args[1:]:
			n = i.eval (contexte)
			s *= n.den
			d *= n.valeur
		return Nombre (s,d)
	
	def inf (contexte, a, b):
		return Nombre.inexact (contexte, a) < Nombre.inexact (contexte, b)
	
	def infeg (contexte, a, b):
		return Nombre.inexact (contexte, a) <= Nombre.inexact (contexte, b)
	
	def sup (contexte, a, b):
		return Nombre.infeg (contexte, b, a)
	
	def supeg (contexte, a, b):
		return Nombre.inf (contexte, b, a)

		
	def tp (contexte, variable):
		if isinstance (variable, Nombre):
			return Atome ("true")
		else:
			return Atome ("false")

class Variable (Cellule):
	""" Une variable """
	def __init__ (self, nom):
		self.nom = nom

	def __str__ (self):
		return "@{}".format (self.nom)
	
	def eval (self, contexte):
		try:
			return contexte.get (self)
		except:
			return Erreur (Atome ("NotFound"), String ("{} n'est pas défini".format (self.nom)))
	
	def tp (contexte, variable):
		if isinstance (variable, Variable):
			return Atome ("true")
		else:
			return Atome ("false")

class Atome (Cellule):
	""" Un atome (mot-clef) 
		
		Créer une superbe gestion 
		de ceux-ci directement 
		dans le tokenizer / parser
		qui permet à chaque 
		Atome d'être un simple 
		numéro ! (pour simplifier
		le travail de comparaison)
	"""
	def __init__ (self, nom):
		self.nom = nom
	
	def eval (self, contexte):
		return self
	
	def __str__ (self):
		return ":{}".format (self.nom)
	
	def tp (contexte, variable):
		if isinstance (variable, Atome):
			return Atome ("true")
		else:
			return Atome ("false")
	
	def vrai (self):
		if self.nom == "true":
			return Atome ("true")
		else:
			return Atome ("false")
		
	def faux (self):
		if self.nom == "false":
			return Atome ("true")
		else:
			return Atome ("false")
	
	def pVrai (self):
		if self.vrai ().nom == "true":
			return True
		else:
			return False
	
	def pFaux (self):
		if self.vrai ().nom == "false":
			return False
		else:
			return True

### -- Structures de données complexes --- 
#
# Il serait bon de créer une structure plus 
# adaptée que les simples listes et utiliser 
# la persistance des donées pour faire des 
# choses comme des HAMT ou des 
# vraies listes ... cf wiki structures 
# persistantes 
### -- 
class Liste (Cellule):
	""" Une liste ... La partie 
		la plus importante 
		de ALisp 
	"""
	def __init__ (self, l):
		self.liste = l
		self.string = False

	def __str__ (self):
		if self.string == False:
			reprs = []
			for i in self.liste:
				reprs.append (str (i))
			self.string = "({})".format (" ".join (reprs))
		return self.string
		
	
	def head (ctx, l):
		return l.liste[0]

	def tail (ctx, l):
		return Liste (l.liste[1:])
	
	def push (ctx, e, l):
		return Liste ([e] + l.liste) # peu efficace
		
	def eval (self, contexte):
		if len (self.liste) <= 0:
			return self
		
		func = self.liste[0] # récupère la fonction à appeler
		
		func = func.eval (contexte)
		
		# Créer une superclasse « callable » ?
		if isinstance (func, Lambda) or isinstance (func, Macro):
			# différent de eval, passe les arguments 
			# et c'est la fonction qui va faire le boulot 
			return func.run (contexte, self.liste[1:]) # appelle la fonction 
		else:
			return Erreur (Atome ("CallError"), String ("Impossible d'appeler {}".format (func)))
			
			
	def tp (contexte, variable):
		if isinstance (variable, Liste):
			return Atome ("true")
		else:
			return Atome ("false")

class Dico (Cellule):
	""" Un dictionnaire """
	def __init__ (self, d):
		self.dico = dict ()
		i = 0
		while i + 1 < len (d):
			self.dico[d[i]] = d[i + 1]
			i = i + 2
		
		self.string = False

	def __str__ (self):
		if self.string == False:
			reprs = []
			for i,j in self.dico.items ():
				reprs.append (str (i))
				reprs.append (str (j))
			self.string = "{" + "{}".format (" ".join (reprs)) + "}"
		
		return self.string 
   
	def eval (self, contexte):
		# oula ... un peu sorti de nul part ça 
		d = {}
		for i in self.dico:
			n = i.eval (contexte)
			d[n] = self.dico[i]
		s = Dico ([])
		s.dico = d
		return s 
	
	def tp (contexte, variable):
		if isinstance (variable, Dico):
			return Atome ("true")
		else:
			return Atome ("false")

class Erreur (Cellule, Exception): # Gérer la remontée rapide !!!
	""" Une erreur ...
		mais il faudrait inventer 
		un système comme python pour
		avoir une remontée dans des 
		blocs « try » et « except » ... 
		à faire !
	"""
	def __init__ (self, tp, msg):
		self.tp = tp
		self.msg = msg
	
	def eval (self, contexte):
		return self
	
	def __str__ (self):
		return "(erreur {} {})".format (self.tp, self.msg)
	
	def tp (contexte, variable):
		if isinstance (variable, Erreur):
			return Atome ("true")
		else:
			return Atome ("false")
	
	# Malheureusement, je n'ai pas trouvé
	# comment ne pas dépendre du système 
	# de python actuellement ... 
	def essai (contexte, expression):
		try:
			return expression.eval (contexte)
		except Erreur as e:
			return e

	def lever (contexte, erreur):
		raise erreur
