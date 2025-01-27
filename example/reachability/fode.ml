(**
 * First order ordinary differential equation `f`:
 * x' = f(x,t)
 *)

module type S =
  functor (Op : Fadbad.OpS with type scalar = float) ->
  sig
    (** [exec x t] eval derivative at state [x] and time [t] *)
    val exec: Op.t array -> Op.t -> Op.t array
  end
