;; exemple de code en alisp

(def factorielle (fun (n)
					(si (egal? n 0) 
						1 
						(* n (factorielle (- n 1))))))

;; Les calculs numériques sont plutôts exacts 

(/ 1 (* 3 4)) ;; retourne 1/12 (la fraction !)

(inexact (/ 1 12)) ;; retourne le flottant résultat 

;; on peut faire des macros !

(def ... 

;; terminer ces exemples 
