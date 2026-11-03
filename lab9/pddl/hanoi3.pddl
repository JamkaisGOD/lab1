; Lab 9, нэмэлт: 3 диск, 3 peg. d1 хамгийн жижиг
(define (problem hanoi3)
  (:domain hanoi)
  (:objects p1 p2 p3 - peg
            d1 d2 d3 - disk)
  (:init (on d3 p1) (on d2 d3) (on d1 d2)
         (clear d1) (clear p2) (clear p3)
         (smaller p1 d1) (smaller p1 d2) (smaller p1 d3)
         (smaller p2 d1) (smaller p2 d2) (smaller p2 d3)
         (smaller p3 d1) (smaller p3 d2) (smaller p3 d3)
         (smaller d2 d1) (smaller d3 d1) (smaller d3 d2))
  (:goal (and (on d3 p3) (on d2 d3) (on d1 d2))))
