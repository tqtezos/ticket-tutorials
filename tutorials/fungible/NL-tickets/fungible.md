
 This tutorial demonstrates the use of NL's fungible ticket contracts(https://gitlab.com/metastatedev/tezos/-/blob/proto-proposal/tests_python/contracts_alpha/mini_scenarios/ticket_builder_fungible.tz and https://gitlab.com/metastatedev/tezos/-/blob/proto-proposal/tests_python/contracts_alpha/mini_scenarios/ticket_wallet_fungible.tz) on Edonet.
 
In this example, the sequence of steps is as follows: 

1. Admin of the Builder contract mints 2 tickets for Alice.
2. Alice sends those 2 tickets seperately to Bob
3. Bob burns the two tickets by sending them to the builders `burn` entrypoint

Builder contract is on edonet at address: "KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x"
Wallet contracts deployed at addresses: "KT1N6VjvuuBfXBbsyMby96zkYeaWuqCto69Q", "KT1AqgENraEg8oro9gJ61mocjRLGBBkya4DQ"

## Address Constants
```
$ ELI="tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW"
$ ALICE="tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv"
$ BOB="tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6"
$ BUILDER_CODE="~/TQ/metastate-tezos/tests_python/contracts/mini_scenarios/ticket_builder_fungible.tz"
$ WALLET_CODE="~/TQ/metastate-tezos/tests_python/contracts/mini_scenarios/ticket_wallet_fungible.tz"
```
## Builder Origination
```
$ tezos-client originate contract ticket_builder_fungible transferring 0 from eli-edo running $BUILDER_CODE --burn-cap 3000 --init "\"$ELI\"" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 2621.376 units (will add 100 for safety)
Estimated storage: 556 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'opPfqoWWcpbDKy5oAGYZLgJh9B41QUjWnv4cosf7QnvMToTNEUk'
Waiting for the operation to be included...
Operation found in block: BMPDwwLTJE2K4yi8ZePAGT51LusscEhk4wuP3smP5cNj8r5BuEB (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
    Fee to the baker: ꜩ0.000359
    Expected counter: 28429
    Gas limit: 1000
    Storage limit: 0 bytes
    Balance updates:
      tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ........... -ꜩ0.000359
      fees(tz2VZZRfyzaFK5EPqUZ8oKTvFx7hC5H18k2b,1) ... +ꜩ0.000359
    Revelation of manager public key:
      Contract: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
      Key: edpkuFmRVhsgwkPbpoHQ7weDYM4gqjRHvChd7tC2F8bMKedwVSxewF
      This revelation was successfully applied
      Consumed gas: 1000
  Manager signed operations:
    From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
    Fee to the baker: ꜩ0.000719
    Expected counter: 28430
    Gas limit: 2722
    Storage limit: 576 bytes
    Balance updates:
      tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ........... -ꜩ0.000719
      fees(tz2VZZRfyzaFK5EPqUZ8oKTvFx7hC5H18k2b,1) ... +ꜩ0.000719
    Origination:
      From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
      Credit: ꜩ0
      Script:
        { parameter
            (or (ticket %burn unit)
                (pair %mint (contract %destination (ticket unit)) (nat %amount))) ;
          storage address ;
          code { AMOUNT ;
                 PUSH mutez 0 ;
                 ASSERT_CMPEQ ;
                 UNPAIR ;
                 IF_LEFT
                   { READ_TICKET ; CAR ; SELF_ADDRESS ; ASSERT_CMPEQ ; DROP ; NIL operation }
                   { DUP @manager 2 ;
                     SENDER ;
                     ASSERT_CMPEQ ;
                     UNPAIR ;
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
          KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x
        Storage size: 299 bytes
        Paid storage size diff: 299 bytes
        Consumed gas: 2621.376
        Balance updates:
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.07475
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.06425

New contract KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x originated.
The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for opPfqoWWcpbDKy5oAGYZLgJh9B41QUjWnv4cosf7QnvMToTNEUk to be included --confirmations 30 --branch BKnkqjuhQjwvyoSeYEpP7SAv12McZ7ivVrJVQkFH5v8uZFPLmvE
and/or an external block explorer.
Contract memorized as ticket_builder_fungible.

$ BUILDER="KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x"

```


## Wallet orignations (Alice and Bob)
```
$ tezos-client originate contract ticket_wallet1 transferring 0 from alice-edo running ~/TQ/metastate-tezos/tests_python/contracts/mini_scenarios/ticket_wallet_fungible.tz --burn-cap 3000 --init "Pair \"$ALICE\" {}" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 4117.713 units (will add 100 for safety)
Estimated storage: 987 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'oojVcNj6rmshWnHeTTG8fdsjkBA9KvYcyiFhQHD3mf2VDvQViVf'
Waiting for the operation to be included...
Operation found in block: BLKaXnieFt1A9CyMaDAorKNH7Nd9o6peJxQQj1LG8thgdStf2dy (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
    Fee to the baker: ꜩ0.000359
    Expected counter: 28430
    Gas limit: 1000
    Storage limit: 0 bytes
    Balance updates:
      tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ........... -ꜩ0.000359
      fees(tz1VpvtSaSxKvykrqajFJTZqCXgoVJ5cKaM1,1) ... +ꜩ0.000359
    Revelation of manager public key:
      Contract: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
      Key: edpkvQJdTEKJ1a3u73JxJXULc2SEnc5ZR6uqWSn3W3Kboyp3x3kmXj
      This revelation was successfully applied
      Consumed gas: 1000
  Manager signed operations:
    From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
    Fee to the baker: ꜩ0.001269
    Expected counter: 28431
    Gas limit: 4218
    Storage limit: 1007 bytes
    Balance updates:
      tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ........... -ꜩ0.001269
      fees(tz1VpvtSaSxKvykrqajFJTZqCXgoVJ5cKaM1,1) ... +ꜩ0.001269
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
          KT1N6VjvuuBfXBbsyMby96zkYeaWuqCto69Q
        Storage size: 730 bytes
        Updated big_maps:
          New map(39) of type (big_map address (ticket unit))
        Paid storage size diff: 730 bytes
        Consumed gas: 4117.713
        Balance updates:
          tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ... -ꜩ0.1825
          tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ... -ꜩ0.06425

New contract KT1N6VjvuuBfXBbsyMby96zkYeaWuqCto69Q originated.
The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for oojVcNj6rmshWnHeTTG8fdsjkBA9KvYcyiFhQHD3mf2VDvQViVf to be included --confirmations 30 --branch BLDahUm5NP6QNsnQytMUdQ5ik6PwTRkL43HZhPsEPXVs2QiS6QB
and/or an external block explorer.
Contract memorized as ticket_wallet1.

$ WALLET1="KT1N6VjvuuBfXBbsyMby96zkYeaWuqCto69Q"

$ tezos-client originate contract ticket_wallet2 transferring 0 from bob-edo running ~/TQ/metastate-tezos/tests_python/contracts/mini_scenarios/ticket_wallet_fungible.tz --burn-cap 3000 --init "Pair \"$BOB\" {}" >> ~/output.txt 2>&1


Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 4117.713 units (will add 100 for safety)
Estimated storage: 987 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'onyGhtkdSrGXH8Tiovr5pusfJ623Gkqe4A5UsNyaUgk38g52mVZ'
Waiting for the operation to be included...
Operation found in block: BLPmoBze88vD3u9Pk7H2SCis7sCwgivxGi6FNAjhxWQCrqhRwPR (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6
    Fee to the baker: ꜩ0.000359
    Expected counter: 28430
    Gas limit: 1000
    Storage limit: 0 bytes
    Balance updates:
      tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6 ........... -ꜩ0.000359
      fees(tz1dAfFc4QAre74yrPU2jFBLcgaAs9MLHryD,1) ... +ꜩ0.000359
    Revelation of manager public key:
      Contract: tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6
      Key: edpkurViEEdstzSsWuDoU77PnKvjKH4LiknkRW27zUjrtu5xhU2Go7
      This revelation was successfully applied
      Consumed gas: 1000
  Manager signed operations:
    From: tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6
    Fee to the baker: ꜩ0.001269
    Expected counter: 28431
    Gas limit: 4218
    Storage limit: 1007 bytes
    Balance updates:
      tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6 ........... -ꜩ0.001269
      fees(tz1dAfFc4QAre74yrPU2jFBLcgaAs9MLHryD,1) ... +ꜩ0.001269
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
          KT1AqgENraEg8oro9gJ61mocjRLGBBkya4DQ
        Storage size: 730 bytes
        Updated big_maps:
          New map(40) of type (big_map address (ticket unit))
        Paid storage size diff: 730 bytes
        Consumed gas: 4117.713
        Balance updates:
          tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6 ... -ꜩ0.1825
          tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6 ... -ꜩ0.06425

New contract KT1AqgENraEg8oro9gJ61mocjRLGBBkya4DQ originated.
The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for onyGhtkdSrGXH8Tiovr5pusfJ623Gkqe4A5UsNyaUgk38g52mVZ to be included --confirmations 30 --branch BLFN5QUvTpr8JLXwXSvWTP5MkNvjJMpBXvfSBRnmELbxXDgvTZg
and/or an external block explorer.
Contract memorized as ticket_wallet2.

$ WALLET2="KT1AqgENraEg8oro9gJ61mocjRLGBBkya4DQ"


```

## Mint 2 tickets to Alice (Wallet1)

```

$ tezos-client transfer 0 from eli-edo to ticket_builder_fungible --entrypoint "mint" --burn-cap 3000 --arg "Pair \"${WALLET1}%receive\" 2" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 12588.716 units (will add 100 for safety)
Estimated storage: 100 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'onfoPL3QJccnVmFkZUgPRYmzDdGd4426oJxa9DqSbCYisfuYFk4'
Waiting for the operation to be included...
Operation found in block: BMRv83Ku4SJx3Rf9VxwsgfhveABsABzq54bqWLNLVtQ3pqBXXG4 (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
    Fee to the baker: ꜩ0.001582
    Expected counter: 28431
    Gas limit: 12689
    Storage limit: 120 bytes
    Balance updates:
      tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ........... -ꜩ0.001582
      fees(tz1ckviCUXRN6GbGLQtZhVszsd64KR4TYcDN,1) ... +ꜩ0.001582
    Transaction:
      Amount: ꜩ0
      From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
      To: KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x
      Entrypoint: mint
      Parameter: (Pair "KT1N6VjvuuBfXBbsyMby96zkYeaWuqCto69Q%receive" 2)
      This transaction was successfully applied
      Updated storage: 0x000008093363b0d4ddfbbcd73f2c7747e4a0fb3a36e4
      Storage size: 299 bytes
      Consumed gas: 6780.511
    Internal operations:
      Transaction:
        Amount: ꜩ0
        From: KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x
        To: KT1N6VjvuuBfXBbsyMby96zkYeaWuqCto69Q
        Entrypoint: receive
        Parameter: (Pair 0x01aaa4f29006915e1c7b6867024c3fa73337caab3700 (Pair Unit 2))
        This transaction was successfully applied
        Updated storage:
          (Pair 0x00006dba164f4293b862a5e2c5ab84888ea8d7f8cbe6 39)
        Updated big_maps:
          Set map(39)[0x01aaa4f29006915e1c7b6867024c3fa73337caab3700] to (Pair 0x01aaa4f29006915e1c7b6867024c3fa73337caab3700 (Pair Unit 2))
        Storage size: 830 bytes
        Paid storage size diff: 100 bytes
        Consumed gas: 5808.205
        Balance updates:
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.025

The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for onfoPL3QJccnVmFkZUgPRYmzDdGd4426oJxa9DqSbCYisfuYFk4 to be included --confirmations 30 --branch BM7boaLUv9Pwp1b3eUFPVWNxhEuCg7mtctxXfT8KpA1SypQPc58
and/or an external block explorer.


```

## Alice sends 1 ticket to Bob (Wallet2). This SPLITs the tickets in Alice's wallet

```
$ tezos-client transfer 0 from alice-edo to ticket_wallet1 --entrypoint "send" --burn-cap 3000 --arg "Pair \"${WALLET2}%receive\" (Pair 1 \"${BUILDER}\")" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 15232.058 units (will add 100 for safety)
Estimated storage: 100 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'ooUXbQYDvoRuQNuv5RXTHo6rYZ631mt91a5iB9gF7NqLFoM4gNd'
Waiting for the operation to be included...
Operation found in block: BLrxEUyzZ5C63c4DnyHrXGrYYMZsitZy9GkYB4rudXaShnjF4MN (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
    Fee to the baker: ꜩ0.00189
    Expected counter: 28432
    Gas limit: 15333
    Storage limit: 120 bytes
    Balance updates:
      tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ........... -ꜩ0.00189
      fees(tz1RomaiWJV3NFDZWTMVR2aEeHknsn3iF5Gi,1) ... +ꜩ0.00189
    Transaction:
      Amount: ꜩ0
      From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
      To: KT1N6VjvuuBfXBbsyMby96zkYeaWuqCto69Q
      Entrypoint: send
      Parameter: (Pair "KT1AqgENraEg8oro9gJ61mocjRLGBBkya4DQ%receive"
                       (Pair 1 "KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x"))
      This transaction was successfully applied
      Updated storage:
        (Pair 0x00006dba164f4293b862a5e2c5ab84888ea8d7f8cbe6 39)
      Updated big_maps:
        Set map(39)[0x01aaa4f29006915e1c7b6867024c3fa73337caab3700] to (Pair 0x01aaa4f29006915e1c7b6867024c3fa73337caab3700 (Pair Unit 1))
      Storage size: 830 bytes
      Consumed gas: 9423.853
    Internal operations:
      Transaction:
        Amount: ꜩ0
        From: KT1N6VjvuuBfXBbsyMby96zkYeaWuqCto69Q
        To: KT1AqgENraEg8oro9gJ61mocjRLGBBkya4DQ
        Entrypoint: receive
        Parameter: (Pair 0x01aaa4f29006915e1c7b6867024c3fa73337caab3700 (Pair Unit 1))
        This transaction was successfully applied
        Updated storage:
          (Pair 0x0000d00811680a0689cbf5d73126943268cba8284fd2 40)
        Updated big_maps:
          Set map(40)[0x01aaa4f29006915e1c7b6867024c3fa73337caab3700] to (Pair 0x01aaa4f29006915e1c7b6867024c3fa73337caab3700 (Pair Unit 1))
        Storage size: 830 bytes
        Paid storage size diff: 100 bytes
        Consumed gas: 5808.205
        Balance updates:
          tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ... -ꜩ0.025

The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for ooUXbQYDvoRuQNuv5RXTHo6rYZ631mt91a5iB9gF7NqLFoM4gNd to be included --confirmations 30 --branch BMSLZhPYcNTUWhaMS5o95XU64xTgaa8zHkk817tiiv7PrHaX1fc
and/or an external block explorer.

```

## Alice sends 1 more ticket to Bob. This one executes JOIN inside Wallet2 (Bob) but no SPLIT in Wallet1 (Alice)
```
$ tezos-client transfer 0 from alice-edo to ticket_wallet1 --entrypoint "send" --burn-cap 3000 --arg "Pair \"${WALLET2}%receive\" (Pair 1 \"${BUILDER}\")" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 15621.500 units (will add 100 for safety)
Estimated storage: no bytes added
Operation successfully injected in the node.
Operation hash is 'oocbQJ4kecucDMPpNpTR9yc8Y9ZVFU5mVDtAbWR7XZWvbE6SdzG'
Waiting for the operation to be included...
Operation found in block: BM18Dh35j4WWEjMrsYFdike3c5qomTxRf9Nu4p3CDKHve5jTV2Q (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
    Fee to the baker: ꜩ0.001929
    Expected counter: 28433
    Gas limit: 15722
    Storage limit: 0 bytes
    Balance updates:
      tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ........... -ꜩ0.001929
      fees(tz1dAfFc4QAre74yrPU2jFBLcgaAs9MLHryD,1) ... +ꜩ0.001929
    Transaction:
      Amount: ꜩ0
      From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
      To: KT1N6VjvuuBfXBbsyMby96zkYeaWuqCto69Q
      Entrypoint: send
      Parameter: (Pair "KT1AqgENraEg8oro9gJ61mocjRLGBBkya4DQ%receive"
                       (Pair 1 "KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x"))
      This transaction was successfully applied
      Updated storage:
        (Pair 0x00006dba164f4293b862a5e2c5ab84888ea8d7f8cbe6 39)
      Updated big_maps:
        Set map(39)[0x01aaa4f29006915e1c7b6867024c3fa73337caab3700] to (Pair 0x01aaa4f29006915e1c7b6867024c3fa73337caab3700 (Pair Unit 0))
      Storage size: 830 bytes
      Consumed gas: 9423.853
    Internal operations:
      Transaction:
        Amount: ꜩ0
        From: KT1N6VjvuuBfXBbsyMby96zkYeaWuqCto69Q
        To: KT1AqgENraEg8oro9gJ61mocjRLGBBkya4DQ
        Entrypoint: receive
        Parameter: (Pair 0x01aaa4f29006915e1c7b6867024c3fa73337caab3700 (Pair Unit 1))
        This transaction was successfully applied
        Updated storage:
          (Pair 0x0000d00811680a0689cbf5d73126943268cba8284fd2 40)
        Updated big_maps:
          Set map(40)[0x01aaa4f29006915e1c7b6867024c3fa73337caab3700] to (Pair 0x01aaa4f29006915e1c7b6867024c3fa73337caab3700 (Pair Unit 2))
        Storage size: 830 bytes
        Consumed gas: 6197.647

The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for oocbQJ4kecucDMPpNpTR9yc8Y9ZVFU5mVDtAbWR7XZWvbE6SdzG to be included --confirmations 30 --branch BKmP94gpaSF1mMW2BJMbdaUBcKFA8qERsXmqMznbf94fM2c9Kgu
and/or an external block explorer.

```

## Bob burns his remaining tickets

```
$ tezos-client transfer 0 from bob-edo to ticket_wallet2 --entrypoint "send" --burn-cap 3000 --arg "Pair \"${BUILDER}%burn\" (Pair 2 \"${BUILDER}\")" >> ~/output.txt 2>&1

Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 11662.954 units (will add 100 for safety)
Estimated storage: no bytes added
Operation successfully injected in the node.
Operation hash is 'opBiMYeizUfqhyMCn1aVKPXrcV9Ppgctenw55NMk9e8VydoRNRJ'
Waiting for the operation to be included...
Operation found in block: BLbpRfDMSCUmnUbbWP4MnqydP5aghBVGERTYQz5PqCdk6D9yjzm (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6
    Fee to the baker: ꜩ0.00153
    Expected counter: 28432
    Gas limit: 11763
    Storage limit: 0 bytes
    Balance updates:
      tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6 ........... -ꜩ0.00153
      fees(tz1cXeGHP8Urj2pQRwpAkCdPGbCdqFUPsQwU,1) ... +ꜩ0.00153
    Transaction:
      Amount: ꜩ0
      From: tz1ebzubQKGg5AJ2z9Ydun9HzLLy4AzngZq6
      To: KT1AqgENraEg8oro9gJ61mocjRLGBBkya4DQ
      Entrypoint: send
      Parameter: (Pair "KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x%burn"
                       (Pair 2 "KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x"))
      This transaction was successfully applied
      Updated storage:
        (Pair 0x0000d00811680a0689cbf5d73126943268cba8284fd2 40)
      Updated big_maps:
        Set map(40)[0x01aaa4f29006915e1c7b6867024c3fa73337caab3700] to (Pair 0x01aaa4f29006915e1c7b6867024c3fa73337caab3700 (Pair Unit 0))
      Storage size: 830 bytes
      Consumed gas: 8011.725
    Internal operations:
      Transaction:
        Amount: ꜩ0
        From: KT1AqgENraEg8oro9gJ61mocjRLGBBkya4DQ
        To: KT1Q9438XGRGQmWFEuoi5heQiASA5eszRi2x
        Entrypoint: burn
        Parameter: (Pair 0x01aaa4f29006915e1c7b6867024c3fa73337caab3700 (Pair Unit 2))
        This transaction was successfully applied
        Updated storage: 0x000008093363b0d4ddfbbcd73f2c7747e4a0fb3a36e4
        Storage size: 299 bytes
        Consumed gas: 3651.229

The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for opBiMYeizUfqhyMCn1aVKPXrcV9Ppgctenw55NMk9e8VydoRNRJ to be included --confirmations 30 --branch BLipixgfb61g5sWakp52db9jEm9msJM5zpX5kn34J8sVBGo2vxZ
and/or an external block explorer.

```
