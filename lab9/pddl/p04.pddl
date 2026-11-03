; Lab 9, p04: 5 блокийн цамхгийг урвуулах
(define (problem p04)
  (:domain blocksworld)
  (:objects a b c d e - block)
  (:init (on a b) (on b c) (on c d) (on d e) (ontable e)
         (clear a)
         (handempty))
  (:goal (and (on e d) (on d c) (on c b) (on b a))))
