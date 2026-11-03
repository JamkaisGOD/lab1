; Lab 9, p02: Sussman anomaly, c нь a дээр
(define (problem p02)
  (:domain blocksworld)
  (:objects a b c - block)
  (:init (on c a) (ontable a) (ontable b)
         (clear c) (clear b)
         (handempty))
  (:goal (and (on a b) (on b c))))
