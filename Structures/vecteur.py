# vecteur.py
#
# Lopez Aliaume
#
# Le vecteur est un tableau
# de taille dynamique plus 
# adapté que celui de python
# pour les petits 
# ajouts et modifications 
#
#
# Implémente itérable


# L'implémentation suit la logique 
# utilisée par Clojure pour son vecteur 
# de même type ... 
#
# Pour le moment c'est un peu fouilli ... 
# il faut le poser sur papier et bien 
# le penser ... 


import trie


class Vecteur:
	def __init__ (self, *values):
		self.len = len (values)
		if values != [None]:
			self.arbre = trie.LookupTree (values)
		else:
			self.arbre = None

	def append (self,elem):
		v = Vecteur (None)
		v.arbre = self.arbre.insert (self.len, elem)
		v.len = self.len + 1
		return v

	def __repr__ (self):
		return self.arbre.__repr__ ()