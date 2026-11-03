; Lab 9, Алхам 7: blocks_domain-ийн эвдэрсэн хувилбар 3
; put-down ба stack-аас (handempty) add хассан
(define (domain blocksworld)
  (:requirements :strips :typing)
  (:types block)
  (:predicates
    (on ?x - block ?y - block)
    (ontable ?x - block)
    (clear ?x - block)
    (holding ?x - block)
    (handempty)
  )

  ; ширээн дээрх блокийг авах
  (:action pick-up
    :parameters (?x - block)
    :precondition (and (clear ?x) (ontable ?x) (handempty))
    :effect (and (holding ?x)
                 (not (ontable ?x))
                 (not (clear ?x))
                 (not (handempty))))

  ; барьж байгаа блокийг ширээнд тавих
  (:action put-down
    :parameters (?x - block)
    :precondition (and (holding ?x))
    :effect (and (ontable ?x)
                 (clear ?x)
                 (not (holding ?x))))

  ; барьж байгаа x-г y дээр тавих
  (:action stack
    :parameters (?x - block ?y - block)
    :precondition (and (holding ?x) (clear ?y))
    :effect (and (on ?x ?y)
                 (clear ?x)
                 (not (holding ?x))
                 (not (clear ?y))))

  ; y дээрх x-г авах
  (:action unstack
    :parameters (?x - block ?y - block)
    :precondition (and (on ?x ?y) (clear ?x) (handempty))
    :effect (and (holding ?x)
                 (clear ?y)
                 (not (on ?x ?y))
                 (not (clear ?x))
                 (not (handempty))))
)
