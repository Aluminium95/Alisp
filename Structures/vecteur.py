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

# Concept :
#
# Un arbre avec à chaque nœud deux 
# branches, et 
import iterable

class Vecteur (Iterable):
	def __init__ (self):
		self.arbre = Node (1)
		self.nbr = 0

	def append (self,elem):
		self.define (self.nbr + 1, elem)
	
	def define (self, i, e):
		if i > self.arbre.maximum:
			a = Node (self.arbre.maximum * 2)
			a.left = self.arbre
			a.right = PartialNode (i,e)
			self.
		else:


class Node:
	def __init__ (self,m):
		self.droite = None
		self.gauche = None
		self.maximum = m
	
	def setDroite (self, n):
		self.droite = n 
	
	def setGauche (self, n):
		self.gauche = n 
	
class PartialNode:
	def __init__ (self):
		
