module Interval = Sets.Interval
module AAF = Sets.AffineForm

module F = Fadbad.F(Interval)

exception Picard_not_contract
let rec picard x0 f dt x nb_max =
  if nb_max <= 0 then
    x
  else
    let next_x = F.(x0 + ((f x) * dt)) in
    if Interval.subset (F.value next_x) (F.value x) then
      picard x0 f dt next_x (nb_max - 1)
    else
      raise Picard_not_contract


let () =
  let open Interval in
  let i1 = {min = -2.3; max = 5.2} in
  let () = Printf.printf "i1 = %s\n" (to_string i1) in
  let i2 = {min = 2.; max = 2.} in
  let () = Printf.printf "i2 = %s\n" (to_string i2) in
  let i3 = i1 ** i2 in
  let () = Printf.printf "i3 = %s\n" (to_string i3) in
  ()

let () =
  let open AAF in
  let e0 = create_noise () in
  let e1 = create_noise () in
  let x1 = (make_float 1.) + e1 in
  let x2 = (make_float 2.) + (scale e1 2.) - e0 in
  let () = Printf.printf "x1 = %s\n" (to_string x1) in
  let () = Printf.printf "x2 = %s\n" (to_string x2) in
  let x3 = x1 * x2 in
  let () = Printf.printf "x1 * x2 = %s\n" (to_string x3) in
  let x4 = x3 - x2 in
  let () = Printf.printf "x1 * x2 - x2 = %s\n" (to_string x4) in
  ()