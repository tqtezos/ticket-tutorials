This tutorial demonstrates a minor modification of the NL ticket contracts in the previous tutorial, to create a contract that wraps tez. A user mints N tickets by calling mint entrypoint of their builder contract and sending N mutez in the operation. They are then free to trade around those tickets to other wallets, like they would tez, all while delegating the tez they deposited to the builder contract. Anyone in posession of these tickets can redeem them for the equivalent amount of tez by sending their tickets to the burn entrypoint of the builder contract. In this way, the user has created a token collateralized by tez that she has full delegation control over

The sequence of steps in the below tutorial is as follows:

1) Eli mints 2,000,000 tickets for Alice while locking 2 tez in his builder contract. 
2) Alice sends 1,000,000 of them to Bob.
3) Alice and Bob burn all of their tickets, each redeeming 1 tez respectively in the process. 


## Set Address Constants
```
$ ELI="\"tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW\""
$ ALICE="\"tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv\""
$ BOB="\"tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6\""
```

## Originate Builder (In practice, user will want to include --delegate flag to delegate locked tez)

```
$ tezos-client originate contract wrapped-builder transferring 0 from eli-edo running ~/TQ/ticket-tutorials/tutorials/fungible/wrapped-tez/builder.tz --burn-cap 3000 --init $ELI >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 3001.262 units (will add 100 for safety)
Estimated storage: 644 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'oooRrd7NFy25jDwfEKy4Rsvun5EQewBcJPyW7ckGatvUtsGZisY'
Waiting for the operation to be included...
Operation found in block: BLT2cDY5cWHxQk2a2v7369A6Mf9RKXKyN7CY4Gw6BhVPFUEerQj (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
    Fee to the baker: ꜩ0.000941
    Expected counter: 28432
    Gas limit: 3102
    Storage limit: 664 bytes
    Balance updates:
      tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ........... -ꜩ0.000941
      fees(tz1cXeGHP8Urj2pQRwpAkCdPGbCdqFUPsQwU,9) ... +ꜩ0.000941
    Origination:
      From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
      Credit: ꜩ0
      Script:
        { parameter
            (or (ticket %burn unit)
                (pair %mint (contract %destination (ticket unit)) (nat %amount))) ;
          storage address ;
          code { UNPAIR ;
                 IF_LEFT
                   { READ_TICKET ;
                     UNPAIR ;
                     SELF_ADDRESS ;
                     ASSERT_CMPEQ ;
                     CDR ;
                     SOURCE ;
                     CONTRACT unit ;
                     IF_NONE
                       { DROP ; PUSH string "contract not found" ; FAILWITH }
                       { SWAP ; PUSH mutez 1 ; MUL ; UNIT ; TRANSFER_TOKENS } ;
                     SWAP ;
                     DROP ;
                     NIL operation ;
                     SWAP ;
                     CONS }
                   { DUP @manager 2 ;
                     SENDER ;
                     ASSERT_CMPEQ ;
                     UNPAIR ;
                     DUP @amount 2 ;
                     PUSH mutez 1 ;
                     MUL ;
                     AMOUNT ;
                     ASSERT_CMPEQ ;
                     SWAP ;
                     UNIT ;
                     TICKET ;
                     PUSH mutez 0 ;
                     SWAP ;
                     TRANSFER_TOKENS ;
                     NIL operation ;
                     SWAP ;
                     CONS } ;
                 PAIR } }
        Initial storage: "tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW"
        No delegate for this contract
        This origination was successfully applied
        Originated contracts:
          KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB
        Storage size: 387 bytes
        Paid storage size diff: 387 bytes
        Consumed gas: 3001.262
        Balance updates:
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.09675
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.06425

New contract KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB originated.
The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for oooRrd7NFy25jDwfEKy4Rsvun5EQewBcJPyW7ckGatvUtsGZisY to be included --confirmations 30 --branch BLDRoSDtFWL1ABD8C3ag2dXwv92swMgRMKNu9MxWHTQ9XmcS3pc
and/or an external block explorer.
Contract memorized as wrapped-builder.

$ BUILDER="KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB"

```

## Originate Wallets

```
$ ./tezos-client originate contract wrapped_wallet1 transferring 0 from alice-edo running ~/TQ/ticket-tutorials/tutorials/fungible/wrapped-tez/wallet.tz --burn-cap 3000 --init "Pair $ALICE {}" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 4117.713 units (will add 100 for safety)
Estimated storage: 987 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'ooUQGaiLhXgY2WRqRza8ne5nzvaR6DnvKYhSG3MYFUamuWiMDsY'
Waiting for the operation to be included...
Operation found in block: BLjr75c9hMWNyWVknbmvRNAobRvmKygDNrMegjgJd3Uw8tQzALb (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
    Fee to the baker: ꜩ0.001365
    Expected counter: 28434
    Gas limit: 4218
    Storage limit: 1007 bytes
    Balance updates:
      tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ........... -ꜩ0.001365
      fees(tz1aWXP237BLwNHJcCD4b3DutCevhqq2T1Z9,9) ... +ꜩ0.001365
    Origination:
      From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
      Credit: ꜩ0
      Script:
        { parameter
            (or (ticket %receive unit)
                (pair %send (contract %destination (ticket unit)) (nat %amount) (address %ticketer))) ;
          storage (pair (address %manager) (big_map %tickets address (ticket unit))) ;
          code { AMOUNT ;
                 PUSH mutez 0 ;
                 ASSERT_CMPEQ ;
                 UNPAIR 3 ;
                 IF_LEFT
                   { READ_TICKET ;
                     CAR @ticketer ;
                     DUP ;
                     DIG 4 ;
                     NONE (ticket unit) ;
                     DIG 2 ;
                     GET_AND_UPDATE ;
                     IF_SOME { DIG 3 ; PAIR ; JOIN_TICKETS ; ASSERT_SOME } { DIG 2 } ;
                     SOME ;
                     DIG 2 ;
                     GET_AND_UPDATE ;
                     ASSERT_NONE ;
                     SWAP ;
                     PAIR ;
                     NIL operation }
                   { DUP @manager 2 ;
                     SENDER ;
                     ASSERT_CMPEQ ;
                     UNPAIR 3 ;
                     DIG 4 ;
                     NONE (ticket unit) ;
                     DUP @ticketer 5 ;
                     GET_AND_UPDATE ;
                     ASSERT_SOME ;
                     READ_TICKET ;
                     GET @total_amount 4 ;
                     DUP @amount 5 ;
                     SWAP ;
                     SUB ;
                     ISNAT ;
                     ASSERT_SOME @remaining_amount ;
                     DIG 4 ;
                     PAIR ;
                     SWAP ;
                     SPLIT_TICKET ;
                     ASSERT_SOME ;
                     UNPAIR @to_send @to_keep ;
                     DUG 5 ;
                     SOME ;
                     DIG 3 ;
                     GET_AND_UPDATE ;
                     ASSERT_NONE ;
                     DIG 2 ;
                     PAIR ;
                     SWAP ;
                     PUSH mutez 0 ;
                     DIG 3 ;
                     TRANSFER_TOKENS ;
                     NIL operation ;
                     SWAP ;
                     CONS } ;
                 PAIR } }
        Initial storage: (Pair "tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv" {})
        No delegate for this contract
        This origination was successfully applied
        Originated contracts:
          KT1HJJ8kbYB1g4XwXewa1NmP6hZehKFDrPX1
        Storage size: 730 bytes
        Updated big_maps:
          New map(60) of type (big_map address (ticket unit))
        Paid storage size diff: 730 bytes
        Consumed gas: 4117.713
        Balance updates:
          tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ... -ꜩ0.1825
          tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ... -ꜩ0.06425

New contract KT1HJJ8kbYB1g4XwXewa1NmP6hZehKFDrPX1 originated.
The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for ooUQGaiLhXgY2WRqRza8ne5nzvaR6DnvKYhSG3MYFUamuWiMDsY to be included --confirmations 30 --branch BL8nAEPwSif4oSuxAAFWYM7AC8siK5L8iVNQ3yTj4do5riwNkDJ
and/or an external block explorer.
Contract memorized as wrapped_wallet1.

$ ./tezos-client originate contract wrapped_wallet2 transferring 0 from bob-edo running ~/TQ/ticket-tutorials/tutorials/fungible/wrapped-tez/wallet.tz --burn-cap 3000 --init "Pair $BOB {}" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 4117.713 units (will add 100 for safety)
Estimated storage: 987 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'ooxoijas4KdQzAuhxws9EtXo5BUDyq47saehn3b2h6aPs9Nrbap'
Waiting for the operation to be included...
Operation found in block: BLxPikKBbwtwQCaR256jiiS9XBWHJFkojAKKDZ2wWbqmjrfMJx5 (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6
    Fee to the baker: ꜩ0.001365
    Expected counter: 28433
    Gas limit: 4218
    Storage limit: 1007 bytes
    Balance updates:
      tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6 ........... -ꜩ0.001365
      fees(tz2VZZRfyzaFK5EPqUZ8oKTvFx7hC5H18k2b,9) ... +ꜩ0.001365
    Origination:
      From: tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6
      Credit: ꜩ0
      Script:
        { parameter
            (or (ticket %receive unit)
                (pair %send (contract %destination (ticket unit)) (nat %amount) (address %ticketer))) ;
          storage (pair (address %manager) (big_map %tickets address (ticket unit))) ;
          code { AMOUNT ;
                 PUSH mutez 0 ;
                 ASSERT_CMPEQ ;
                 UNPAIR 3 ;
                 IF_LEFT
                   { READ_TICKET ;
                     CAR @ticketer ;
                     DUP ;
                     DIG 4 ;
                     NONE (ticket unit) ;
                     DIG 2 ;
                     GET_AND_UPDATE ;
                     IF_SOME { DIG 3 ; PAIR ; JOIN_TICKETS ; ASSERT_SOME } { DIG 2 } ;
                     SOME ;
                     DIG 2 ;
                     GET_AND_UPDATE ;
                     ASSERT_NONE ;
                     SWAP ;
                     PAIR ;
                     NIL operation }
                   { DUP @manager 2 ;
                     SENDER ;
                     ASSERT_CMPEQ ;
                     UNPAIR 3 ;
                     DIG 4 ;
                     NONE (ticket unit) ;
                     DUP @ticketer 5 ;
                     GET_AND_UPDATE ;
                     ASSERT_SOME ;
                     READ_TICKET ;
                     GET @total_amount 4 ;
                     DUP @amount 5 ;
                     SWAP ;
                     SUB ;
                     ISNAT ;
                     ASSERT_SOME @remaining_amount ;
                     DIG 4 ;
                     PAIR ;
                     SWAP ;
                     SPLIT_TICKET ;
                     ASSERT_SOME ;
                     UNPAIR @to_send @to_keep ;
                     DUG 5 ;
                     SOME ;
                     DIG 3 ;
                     GET_AND_UPDATE ;
                     ASSERT_NONE ;
                     DIG 2 ;
                     PAIR ;
                     SWAP ;
                     PUSH mutez 0 ;
                     DIG 3 ;
                     TRANSFER_TOKENS ;
                     NIL operation ;
                     SWAP ;
                     CONS } ;
                 PAIR } }
        Initial storage: (Pair "tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6" {})
        No delegate for this contract
        This origination was successfully applied
        Originated contracts:
          KT1TDFT1KN26daV6gEazd7XBr4cAP9VkhkLu
        Storage size: 730 bytes
        Updated big_maps:
          New map(61) of type (big_map address (ticket unit))
        Paid storage size diff: 730 bytes
        Consumed gas: 4117.713
        Balance updates:
          tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6 ... -ꜩ0.1825
          tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6 ... -ꜩ0.06425

New contract KT1TDFT1KN26daV6gEazd7XBr4cAP9VkhkLu originated.
The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for ooxoijas4KdQzAuhxws9EtXo5BUDyq47saehn3b2h6aPs9Nrbap to be included --confirmations 30 --branch BLjDUvrrLvRyUE2eSAijurRGwSP5o95rTfgveHbV1QBPvB8thGd
and/or an external block explorer.
Contract memorized as wrapped_wallet2.


$ WALLET1="KT1HJJ8kbYB1g4XwXewa1NmP6hZehKFDrPX1"
$ WALLET2="KT1TDFT1KN26daV6gEazd7XBr4cAP9VkhkLu"
```

## Mint of of 2,000,000 tickets without locking an equal amount of mutez (2 tez) fails

```
$ ./tezos-client transfer 0 from eli-edo to wrapped-builder --entrypoint "mint" --burn-cap 3000 --arg "Pair \"${WALLET1}%receive\" 2000000" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
This simulation failed:
  Manager signed operations:
    From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
    Fee to the baker: ꜩ0
    Expected counter: 28433
    Gas limit: 1040000
    Storage limit: 60000 bytes
    Transaction:
      Amount: ꜩ0
      From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
      To: KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB
      Entrypoint: mint
      Parameter: (Pair "KT1HJJ8kbYB1g4XwXewa1NmP6hZehKFDrPX1%receive" 2000000)
      This operation FAILED.

Runtime error in contract KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB:
  01: { parameter
  02:     (or (ticket %burn unit)
  03:         (pair %mint (contract %destination (ticket unit)) (nat %amount))) ;
  04:   storage address ;
  05:   code { UNPAIR ;
  06:          IF_LEFT
  07:            { READ_TICKET ;
  08:              UNPAIR ;
  09:              SELF_ADDRESS ;
  10:              ASSERT_CMPEQ ;
  11:              CDR ;
  12:              SOURCE ;
  13:              CONTRACT unit ;
  14:              IF_NONE
  15:                { DROP ; PUSH string "contract not found" ; FAILWITH }
  16:                { SWAP ; PUSH mutez 1 ; MUL ; UNIT ; TRANSFER_TOKENS } ;
  17:              SWAP ;
  18:              DROP ;
  19:              NIL operation ;
  20:              SWAP ;
  21:              CONS }
  22:            { DUP @manager 2 ;
  23:              SENDER ;
  24:              ASSERT_CMPEQ ;
  25:              UNPAIR ;
  26:              DUP @amount 2 ;
  27:              PUSH mutez 1 ;
  28:              MUL ;
  29:              AMOUNT ;
  30:              ASSERT_CMPEQ ;
  31:              SWAP ;
  32:              UNIT ;
  33:              TICKET ;
  34:              PUSH mutez 0 ;
  35:              SWAP ;
  36:              TRANSFER_TOKENS ;
  37:              NIL operation ;
  38:              SWAP ;
  39:              CONS } ;
  40:          PAIR } }
At line 30 characters 13 to 25,
script reached FAILWITH instruction
with Unit
Fatal error:
  transfer simulation failed

```
## Minting 2,000,000 tickets succeeds when we lock 2 tez

```
$ ./tezos-client transfer 2 from eli-edo to wrapped-builder --entrypoint "mint" --burn-cap 3000 --arg "Pair \"${WALLET1}%receive\" 2000000" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 12759.219 units (will add 100 for safety)
Estimated storage: 103 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'ooJrLx3bJqz51vFyoVxKoKUuKoZMwq2gXq2UWsh2TYbT8QVipsq'
Waiting for the operation to be included...
Operation found in block: BMNyVvLx4pEr1fAeaE12gDwgqktu7PYBTxYRyzHUpr32r1jZqtD (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
    Fee to the baker: ꜩ0.001604
    Expected counter: 28433
    Gas limit: 12860
    Storage limit: 123 bytes
    Balance updates:
      tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ........... -ꜩ0.001604
      fees(tz2VZZRfyzaFK5EPqUZ8oKTvFx7hC5H18k2b,9) ... +ꜩ0.001604
    Transaction:
      Amount: ꜩ2
      From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
      To: KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB
      Entrypoint: mint
      Parameter: (Pair "KT1HJJ8kbYB1g4XwXewa1NmP6hZehKFDrPX1%receive" 2000000)
      This transaction was successfully applied
      Updated storage: 0x000008093363b0d4ddfbbcd73f2c7747e4a0fb3a36e4
      Storage size: 387 bytes
      Consumed gas: 6951.002
      Balance updates:
        tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ2
        KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB ... +ꜩ2
    Internal operations:
      Transaction:
        Amount: ꜩ0
        From: KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB
        To: KT1HJJ8kbYB1g4XwXewa1NmP6hZehKFDrPX1
        Entrypoint: receive
        Parameter: (Pair 0x01a44df1e6ea1964307afcc67490eb71a67f95214600 (Pair Unit 2000000))
        This transaction was successfully applied
        Updated storage:
          (Pair 0x00006dba164f4293b862a5e2c5ab84888ea8d7f8cbe6 60)
        Updated big_maps:
          Set map(60)[0x01a44df1e6ea1964307afcc67490eb71a67f95214600] to (Pair 0x01a44df1e6ea1964307afcc67490eb71a67f95214600 (Pair Unit 2000000))
        Storage size: 833 bytes
        Paid storage size diff: 103 bytes
        Consumed gas: 5808.217
        Balance updates:
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.02575

The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for ooJrLx3bJqz51vFyoVxKoKUuKoZMwq2gXq2UWsh2TYbT8QVipsq to be included --confirmations 30 --branch BLnSwAz6TCxtBsTTLauxpCfPd3U4toSWx9mkQ4ZNNQjXxUWupHr
and/or an external block explorer.

```

## Transfer 1,000,000 tickets from alice's wallet to bob's wallet

```
$ ./tezos-client transfer 0 from alice-edo to wrapped_wallet1 --entrypoint "send" --burn-cap 3000 --arg "Pair \"${WALLET2}%receive\" (Pair 1000000 \"${BUILDER}\")" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 15232.080 units (will add 100 for safety)
Estimated storage: 102 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'ooGSv9PHZhKzmWNLWVcVoZfyMDabs8fksDuysBcTJNtr4hVfmbU'
Waiting for the operation to be included...
Operation found in block: BLRqFeEjHk4LeHpdXK1gmf9zmErCC3P1e5Xc92c8R1qS5tKR1aP (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
    Fee to the baker: ꜩ0.001892
    Expected counter: 28435
    Gas limit: 15333
    Storage limit: 122 bytes
    Balance updates:
      tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ........... -ꜩ0.001892
      fees(tz1RomaiWJV3NFDZWTMVR2aEeHknsn3iF5Gi,9) ... +ꜩ0.001892
    Transaction:
      Amount: ꜩ0
      From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
      To: KT1HJJ8kbYB1g4XwXewa1NmP6hZehKFDrPX1
      Entrypoint: send
      Parameter: (Pair "KT1TDFT1KN26daV6gEazd7XBr4cAP9VkhkLu%receive"
                       (Pair 1000000 "KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB"))
      This transaction was successfully applied
      Updated storage:
        (Pair 0x00006dba164f4293b862a5e2c5ab84888ea8d7f8cbe6 60)
      Updated big_maps:
        Set map(60)[0x01a44df1e6ea1964307afcc67490eb71a67f95214600] to (Pair 0x01a44df1e6ea1964307afcc67490eb71a67f95214600 (Pair Unit 1000000))
      Storage size: 832 bytes
      Consumed gas: 9423.867
    Internal operations:
      Transaction:
        Amount: ꜩ0
        From: KT1HJJ8kbYB1g4XwXewa1NmP6hZehKFDrPX1
        To: KT1TDFT1KN26daV6gEazd7XBr4cAP9VkhkLu
        Entrypoint: receive
        Parameter: (Pair 0x01a44df1e6ea1964307afcc67490eb71a67f95214600 (Pair Unit 1000000))
        This transaction was successfully applied
        Updated storage:
          (Pair 0x0000d00811680a0689cbf5d73126943268cba8284fd2 61)
        Updated big_maps:
          Set map(61)[0x01a44df1e6ea1964307afcc67490eb71a67f95214600] to (Pair 0x01a44df1e6ea1964307afcc67490eb71a67f95214600 (Pair Unit 1000000))
        Storage size: 832 bytes
        Paid storage size diff: 102 bytes
        Consumed gas: 5808.213
        Balance updates:
          tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ... -ꜩ0.0255

The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for ooGSv9PHZhKzmWNLWVcVoZfyMDabs8fksDuysBcTJNtr4hVfmbU to be included --confirmations 30 --branch BLLncUiVnYXbAB27z1JASgBiiMHRYc1igYmdH8grRshETFckp1p
and/or an external block explorer.
```

## Alice and Bob burn all of their tickets and redeem 1 tez each from builder contract

```
$ ./tezos-client transfer 0 from alice-edo to wrapped_wallet1 --entrypoint "send" --burn-cap 3000 --arg "Pair \"${BUILDER}%burn\" (Pair 1000000 \"${BUILDER}\")" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 14082.265 units (will add 100 for safety)
Estimated storage: no bytes added
Operation successfully injected in the node.
Operation hash is 'op5CMb4MTNftE4R9qWVcU4nc57GHWgBFYLt1rMbrk4x8ALNQqtD'
Waiting for the operation to be included...
Operation found in block: BKr8Uaco3uVQ7uk3GofLmeVgMHzRWT1TP91kukSGHJ1zYkc4V9i (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
    Fee to the baker: ꜩ0.001774
    Expected counter: 28436
    Gas limit: 14183
    Storage limit: 0 bytes
    Balance updates:
      tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ........... -ꜩ0.001774
      fees(tz1YCABRTa6H8PLKx2EtDWeCGPaKxUhNgv47,9) ... +ꜩ0.001774
    Transaction:
      Amount: ꜩ0
      From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
      To: KT1HJJ8kbYB1g4XwXewa1NmP6hZehKFDrPX1
      Entrypoint: send
      Parameter: (Pair "KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB%burn"
                       (Pair 1000000 "KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB"))
      This transaction was successfully applied
      Updated storage:
        (Pair 0x00006dba164f4293b862a5e2c5ab84888ea8d7f8cbe6 60)
      Updated big_maps:
        Set map(60)[0x01a44df1e6ea1964307afcc67490eb71a67f95214600] to (Pair 0x01a44df1e6ea1964307afcc67490eb71a67f95214600 (Pair Unit 0))
      Storage size: 830 bytes
      Consumed gas: 8376.905
    Internal operations:
      Transaction:
        Amount: ꜩ0
        From: KT1HJJ8kbYB1g4XwXewa1NmP6hZehKFDrPX1
        To: KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB
        Entrypoint: burn
        Parameter: (Pair 0x01a44df1e6ea1964307afcc67490eb71a67f95214600 (Pair Unit 1000000))
        This transaction was successfully applied
        Updated storage: 0x000008093363b0d4ddfbbcd73f2c7747e4a0fb3a36e4
        Storage size: 387 bytes
        Consumed gas: 4278.360
      Transaction:
        Amount: ꜩ1
        From: KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB
        To: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
        This transaction was successfully applied
        Consumed gas: 1427
        Balance updates:
          KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB ... -ꜩ1
          tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ... +ꜩ1

The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for op5CMb4MTNftE4R9qWVcU4nc57GHWgBFYLt1rMbrk4x8ALNQqtD to be included --confirmations 30 --branch BLvXLZ4zDt4tgsHGWUv1qBcrPkuYA1yx7Do1BEQFid12UfbyCBN
and/or an external block explorer.

$ ./tezos-client transfer 0 from bob-edo to wrapped_wallet2 --entrypoint "send" --burn-cap 3000 --arg "Pair \"${BUILDER}%burn\" (Pair 1000000 \"${BUILDER}\")" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 14082.265 units (will add 100 for safety)
Estimated storage: no bytes added
Operation successfully injected in the node.
Operation hash is 'ooQmyHYtbJS7XB6bvxJFwoEVCenFec92rAsWwJYaseByytqEaKA'
Waiting for the operation to be included...
Operation found in block: BLR1CuPjBvgpsN65tCUGH56fnFLdY6CmheE2khu79wBAXhZeWiA (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6
    Fee to the baker: ꜩ0.001774
    Expected counter: 28434
    Gas limit: 14183
    Storage limit: 0 bytes
    Balance updates:
      tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6 ........... -ꜩ0.001774
      fees(tz1RomaiWJV3NFDZWTMVR2aEeHknsn3iF5Gi,9) ... +ꜩ0.001774
    Transaction:
      Amount: ꜩ0
      From: tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6
      To: KT1TDFT1KN26daV6gEazd7XBr4cAP9VkhkLu
      Entrypoint: send
      Parameter: (Pair "KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB%burn"
                       (Pair 1000000 "KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB"))
      This transaction was successfully applied
      Updated storage:
        (Pair 0x0000d00811680a0689cbf5d73126943268cba8284fd2 61)
      Updated big_maps:
        Set map(61)[0x01a44df1e6ea1964307afcc67490eb71a67f95214600] to (Pair 0x01a44df1e6ea1964307afcc67490eb71a67f95214600 (Pair Unit 0))
      Storage size: 830 bytes
      Consumed gas: 8376.905
    Internal operations:
      Transaction:
        Amount: ꜩ0
        From: KT1TDFT1KN26daV6gEazd7XBr4cAP9VkhkLu
        To: KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB
        Entrypoint: burn
        Parameter: (Pair 0x01a44df1e6ea1964307afcc67490eb71a67f95214600 (Pair Unit 1000000))
        This transaction was successfully applied
        Updated storage: 0x000008093363b0d4ddfbbcd73f2c7747e4a0fb3a36e4
        Storage size: 387 bytes
        Consumed gas: 4278.360
      Transaction:
        Amount: ꜩ1
        From: KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB
        To: tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6
        This transaction was successfully applied
        Consumed gas: 1427
        Balance updates:
          KT1PZXkw968qQ6Gy8kN1nDbKmyMG2edhpncB ... -ꜩ1
          tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6 ... +ꜩ1

The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for ooQmyHYtbJS7XB6bvxJFwoEVCenFec92rAsWwJYaseByytqEaKA to be included --confirmations 30 --branch BKr8Uaco3uVQ7uk3GofLmeVgMHzRWT1TP91kukSGHJ1zYkc4V9i
and/or an external block explorer.

```
