; Lab 9, нэмэлт: 4 диск, 3 peg
(define (problem hanoi4)
  (:domain hanoi)
  (:objects p1 p2 p3 - peg
            d1 d2 d3 d4 - disk)
  (:init (on d4 p1) (on d3 d4) (on d2 d3) (on d1 d2)
         (clear d1) (clear p2) (clear p3)
         (smaller p1 d1) (smaller p1 d2) (smaller p1 d3) (smaller p1 d4)
         (smaller p2 d1) (smaller p2 d2) (smaller p2 d3) (smaller p2 d4)
         (smaller p3 d1) (smaller p3 d2) (smaller p3 d3) (smaller p3 d4)
         (smaller d2 d1) (smaller d3 d1) (smaller d4 d1)
         (smaller d3 d2) (smaller d4 d2) (smaller d4 d3))
  (:goal (and (on d4 p3) (on d3 d4) (on d2 d3) (on d1 d2))))
