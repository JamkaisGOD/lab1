; Lab 9, Алхам 1: гэрэл асаах хамгийн жижиг domain
(define (domain light)
  (:requirements :strips)
  (:predicates (on ?l) (off ?l))
  (:action turn-on
    :parameters (?l)
    :precondition (off ?l)
    :effect (and (on ?l) (not (off ?l)))))
