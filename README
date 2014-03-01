# Alisp

## Concepts et bases 

Alisp est un langage descendant de Lisp, dont la 
syntaxe est claire et épurée.

Tout est une liste, le code est une donnée qui peut 
être traitée comme les autres.

Les variables sont immuables, pour éviter les problèmes 
dans la gestion des processus paralleles qui vont arriver
par la suite

## Organisation du code 

### Un compilateur 

Pour compiler on doit :
	1/ Tokenizer : c'est à dire reconnaitre les mots et les formes syntaxiques 
	2/ Parser : c'est à dire créer un arbre de syntaxe abstrait à partir des mots 
				et de la grammaire du langage
	3/ Executer : c'est à dire réduire l'arbre jusqu'à avoir un résultat 

Mais il ne faut pas oublier qu'un langage possède : 
	- Des types 
	- Des fonctions de base 
	- etc ...

Le code est donc réparti selon le schéma suivant : 
	
	[tokenizer.py] = lecture d'une chaine et produit une liste des mots 
	[parser.py] = permet de créer un AST
	[cellule.py] = Les éléments qui forment l'AST ! Les « cellules » du programme 
	[contexte.py] = gestion du contexte d'exécution : les variables locales 
	[executeur.py] = fonctions de base et exécution 
	[repl.py] = une ReadEvalPrintLoop qui permet de tester le langage


Le tout est assez commenté normalement 
