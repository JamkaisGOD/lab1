; Lab 9, нэмэлт: Hanoi цамхаг
; smaller нь статик баримт, жижиг диск том зүйл дээр л тавигдана
(define (domain hanoi)
  (:requirements :strips :typing)
  (:types place - object
          peg disk - place)
  (:predicates
    (on ?d - disk ?x - place)
    (clear ?x - place)
    (smaller ?x - place ?d - disk)
  )

  ; d-г from дээрээс to руу шилжүүлэх
  (:action move
    :parameters (?d - disk ?from - place ?to - place)
    :precondition (and (on ?d ?from) (clear ?d) (clear ?to) (smaller ?to ?d))
    :effect (and (on ?d ?to)
                 (clear ?from)
                 (not (on ?d ?from))
                 (not (clear ?to))))
)
