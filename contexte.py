#-*- coding: utf-8 --
# contexte.py
# 
# Lopez Aliaume
#
# Le contexte d'éxécution d'un programme 

# TODO:
# 	Problème de performance 
# 	avec la copie de contextes !
# 		- Utiliser une structure sous forme d'arbre, ou avec des FatNodes
#
#   Déterminer le toplevel ! En effet il ne faut 
# 	JAMAIS copier le toplevel (inefficace) parce que 
# 	sinon on ne peut pas utiliser des variables « globales » 

class Contexte:
	def __init__ (self, ctx = {}, toplevel = False):
		self.bindings = {}
		self.toplevel = toplevel 
		self.nbrbinds = 0

		if isinstance (ctx, Contexte):
			for i in ctx.bindings:
				self.bindings[i] = ctx.bindings[i]
				self.nbrbinds += 1
		elif isinstance (ctx, dict):
			self.bindings = ctx

	def set (self, symbole, variable):
		if not symbole in self.bindings: # aaaarrrrgghh looooonnnnggggg
			self.nbrbinds += 1
		self.bindings[symbole] = variable

	def get (self, symbole):
		return self.bindings[symbole]
		
	# Définir des manières de mieux faire une 
	# fusion sans copier intégralement un 
	# dictionnaire de valeurs 
	
	def fusion (self, other):
		# une petite optimisation : si on ajoute
		# rien ... pas besoin de copier !
		if other.nbrbinds == 0:
			return self
		
		if self.nbrbinds == 0:
			return other

		d = {}
		for i in other.bindings:
			d[i] = other.bindings[i]
		
		for i in self.bindings:
			d[i] = self.bindings[i]
			
		return Contexte (d)
