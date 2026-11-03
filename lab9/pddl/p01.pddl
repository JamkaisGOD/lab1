; Lab 9, p01: гурван блок ширээн дээр, a-b-c цамхаг босгох
(define (problem p01)
  (:domain blocksworld)
  (:objects a b c - block)
  (:init (ontable a) (ontable b) (ontable c)
         (clear a) (clear b) (clear c)
         (handempty))
  (:goal (and (on a b) (on b c))))
