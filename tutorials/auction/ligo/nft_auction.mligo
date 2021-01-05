type storage =
  [@layout:comb]
  {admin : address;
   current_price : nat;
   reserve_price : nat;
   in_progress : bool;
   start_time : timestamp;
   round_time : int;
   ticket : (nat, nat ticket) big_map}

type configure_parameter =
  [@layout:comb]
  {opening_price : nat;
  reserve_price : nat;
  start_time : timestamp;
  round_time : int;
  ticket : (nat ticket)}

type parameter =
  | Configure of configure_parameter
  | Start of unit
  | Drop_price of nat
  | Buy of (nat ticket contract)
  | Cancel of (nat ticket contract)

let main (arg : parameter * storage) : operation list * storage =
  begin
    let (p,storage) = arg in
    let {admin = admin; current_price = current_price; reserve_price = reserve_price; in_progress = in_progress; start_time = start_time; round_time = round_time; ticket = ticket} = storage in
    ( match p with
        | Configure configure -> begin
            assert (Tezos.source = admin);
            assert (not in_progress);
            let ticket = Big_map.update 0n (Some configure.ticket) ticket in
            (([] : operation list), {admin = admin; current_price = configure.opening_price; reserve_price = configure.reserve_price;
            in_progress = in_progress; start_time = configure.start_time; round_time = configure.round_time; ticket = ticket})
          end
        | Start -> begin
            let now = Tezos.now in
            assert (Tezos.source = admin);
            assert (not in_progress);
            assert (now >= start_time);
            ( match (Big_map.find_opt 0n ticket) with
               | None -> (failwith "no ticket" : operation list * storage)
               | Some t ->
                 (([] : operation list), {storage with in_progress = true; start_time = now})
            )
          end
        | Drop_price new_price -> begin
            let now = Tezos.now in
            assert (Tezos.sender = admin);
            assert (in_progress);
            (* assert (new_price < current_price); *)
            assert (new_price >= reserve_price);
            assert (now > start_time +  round_time);
            (([] : operation list), {storage with current_price = new_price; start_time = now})
          end
        | Buy send_to -> begin
            let now = Tezos.now in
            let purchase_price = Tezos.amount in
            assert (Tezos.sender <> admin);
            assert (in_progress);
            assert (purchase_price = (current_price * 1mutez));
            assert (now <= start_time +  round_time);
            ( match ((Tezos.get_contract_opt admin) : unit contract option) with
                | None -> (failwith "contract does not match" : operation list * storage)
                | Some c -> let op1 = Tezos.transaction () purchase_price c in
                    let (t, ticket) = Big_map.get_and_update 0n (None : nat ticket option) ticket in
                    ( match t with
                        | None -> (failwith "ticket does not exist" : operation list * storage)
                        | Some t -> let op2 = Tezos.transaction t 0mutez send_to in
                           ([op1; op2], {storage with ticket = ticket; in_progress = false})
                    )
            )
          end
        | Cancel return_destination -> begin
            assert (Tezos.sender = admin);
            assert (in_progress);
            let (t, ticket) = Big_map.get_and_update 0n (None : nat ticket option) ticket in
            ( match t with
                | None -> (failwith "ticket does not exist" : operation list * storage)
                | Some t -> let op = Tezos.transaction t 0mutez return_destination in
                    ([op], {storage with in_progress = false; ticket = ticket})
            )
          end
    )
  end
