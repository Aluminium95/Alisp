
(* type récursif node ...
 *  'a est un paramètre de type. Ainsi on peut 
 *  dire que l'on a un « int inode » etc ...
 *)
type 'a inode = Node of int * 'a inode * 'a inode 
    | Leaf of 'a 
    | Empty 
    | Right of int * 'a inode
    | Left of int * 'a inode;;

(* Left (n,a) = Node (n, a, Empty) *)
(* Right (n,a) = Node (n, Empty, a) *)

(* On va à droite par divisions par deux ? *)
let va_droite n i = 
    if (2 lsl (n-1)) < i then 
        true
    else
        false;;

let suppr_droite n i = 
    i - (2 lsl (n-1));;

let rec get t i = (* récupère l'élément i dans t *)
    match t with 
        | Node (n, a, b) -> 
                (if va_droite n i then 
                    get b (suppr_droite n i)
                else
                    get a i)
        | Left (n,a) -> get a i
        | Right (n,a) -> get a (suppr_droite n i)
        | Leaf (a) -> a (* pas le choix *)
        | Empty -> failwith "La clef n'existe pas ...";;


(* Il faut gérer l'ajout dans l'arbre ....
 * C'est à dire la gestion de ce qui est 
 * augmentation du nombre de branches ...
 *)
let rec insert t i e = (* insère l'élément e dans t à i *)
    match t with
        (* Trop grand -> agrandit le tableau *)
        | Node (n,_,_) | Left (n, _) | Right (n, _)
            when (2 lsl n <= i) ->
                insert (Node (n + 1, t, Left (n, Empty))) i e
        | Left (0,Empty) | Right (0,Empty) ->
                (if va_droite 0 i then 
                    Right (0, Leaf (e))
                else
                    Left (0, Leaf (e)))
        | Left (0,a) ->
                (if va_droite 0 i then 
                    Node (0,a,Leaf (e))
                else
                    Left (0,Leaf (e)))
        | Right (0,a) ->
                (if va_droite 0 i then 
                    Right (0,Leaf (e))
                else
                    Node (0,Leaf (e),a))
        | Left (n,Empty) ->
                (if va_droite n i then 
                    Left (n, (insert (Right (n,Empty)) i e (* redirection *)
                else
                    insert (Left (n-1,Empty)) i e)
        | Right (n,Empty) ->
                (if va_droite n i then
                    insert (Right (n-1,Empty)) (suppr_droite n i) e
                else
                    insert (Left (n,Empty)) i e)
        | Left (n,Leaf (a)) ->
                (if va_droite n i then 
                    insert (Node (n, (Left (n-1,Leaf (a))), (Left (n-1,Empty)))) i e
                else
                    Left (n, (insert (Left(n-1,Leaf (a))) i e)))
        | Right (n,Leaf (a)) ->
                (if va_droite n i then 
                    Right (n, (insert (Right (n-1,Leaf(a))) (suppr_droite n i) e))
                else
                    insert (Node (n, (Left (n-1,Empty)), (Right (n-1,Leaf (a))))) i e)
        | Left (n,a) ->
                (if va_droite n i then 
                    Node (n,a, (insert (Right (n-1,Empty)) (suppr_droite n i) e))
                else
                    Left (n, (insert a i e)))
        | Right (n,a) ->
                (if va_droite n i then 
                    Right (n, (insert a (suppr_droite n i) e))
                else
                    Node (n,(insert (Left (n-1,Empty)) i e),a))
        | Node (n, a, b) ->
                (if va_droite n i then
                    Node (n, a, insert b (suppr_droite n i) e)
                else
                    Node (n, insert a i e, b))
        | Leaf (a) -> Leaf (e)
        | Empty -> Leaf (e);;

let exemple = Node (1, Node (0, Leaf (0), Leaf (1)), Node (0, Leaf (2), Leaf (3)));;

let test_insert v n = 
    let rec loop e k = match k with 
        | 0 -> e
        | _ -> loop (insert e k k) (k - 1)
    in
    loop v n;;
