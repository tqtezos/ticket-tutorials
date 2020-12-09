Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 18496.784 units (will add 100 for safety)
Estimated storage: 4077 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'ooMsoty6HNztjafUJrkSPJYBskzxQwyeUvXJ9TWJSWJMFWxfLe6'
Waiting for the operation to be included...
Operation found in block: BLrp8sJtirpGHBRtzkVUkv4cawYSuEia9PVT16m2bXy7GBrfqH9 (pass: 3, offset: 1)
This sequence of operations was run:
  Manager signed operations:
    From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
    Fee to the baker: ꜩ0.005893
    Expected counter: 28434
    Gas limit: 18597
    Storage limit: 4097 bytes
    Balance updates:
      tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ............ -ꜩ0.005893
      fees(tz1ckviCUXRN6GbGLQtZhVszsd64KR4TYcDN,12) ... +ꜩ0.005893
    Origination:
      From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
      Credit: ꜩ0
      Script:
        { parameter
            (or (or (or (pair %approve (address %spender) (nat %value))
                        (pair %burn (address %address) (nat %value)))
                    (or (pair %getAdministrator unit (contract address))
                        (or (pair %getAllowance (pair (address %owner) (address %spender)) (contract nat))
                            (pair %getBalance address (contract (pair (ticket address) nat))))))
                (or (or (pair %getTotalSupply unit (contract nat))
                        (pair %mint (address %address) (nat %value)))
                    (or (address %setAdministrator)
                        (or (bool %setPause) (pair %transfer (address %from) (pair (address %to) (nat %value))))))) ;
          storage
            (pair (pair (address %administrator)
                        (big_map %balances address (pair (map %approvals address nat) (nat %balance))))
                  (pair (bool %paused) (nat %totalSupply))) ;
          code { DUP ;
                 CDR ;
                 SWAP ;
                 CAR ;
                 IF_LEFT
                   { IF_LEFT
                       { IF_LEFT
                           { SWAP ;
                             DUP ;
                             DUG 2 ;
                             CDAR ;
                             IF { PUSH string "WrongCondition: ~ self.data.paused" ; FAILWITH } {} ;
                             PUSH nat 0 ;
                             DIG 2 ;
                             DUP ;
                             DUG 3 ;
                             CADR ;
                             SENDER ;
                             GET ;
                             IF_SOME {} { PUSH int 28 ; FAILWITH } ;
                             CAR ;
                             DIG 2 ;
                             DUP ;
                             DUG 3 ;
                             CAR ;
                             GET ;
                             IF_SOME {} { PUSH nat 0 } ;
                             COMPARE ;
                             EQ ;
                             IF { PUSH bool True } { DUP ; CDR ; PUSH nat 0 ; COMPARE ; EQ } ;
                             IF {} { PUSH string "UnsafeAllowanceChange" ; FAILWITH } ;
                             SWAP ;
                             DUP ;
                             CDR ;
                             SWAP ;
                             CAR ;
                             DUP ;
                             CAR ;
                             SWAP ;
                             CDR ;
                             DUP ;
                             SENDER ;
                             DUP ;
                             DUG 2 ;
                             GET ;
                             IF_SOME {} { PUSH int 30 ; FAILWITH } ;
                             DUP ;
                             CDR ;
                             SWAP ;
                             CAR ;
                             DIG 6 ;
                             DUP ;
                             CAR ;
                             SWAP ;
                             CDR ;
                             SOME ;
                             SWAP ;
                             UPDATE ;
                             PAIR ;
                             SOME ;
                             SWAP ;
                             UPDATE ;
                             SWAP ;
                             PAIR ;
                             PAIR }
                           { SWAP ;
                             DUP ;
                             DUG 2 ;
                             CAAR ;
                             SENDER ;
                             COMPARE ;
                             EQ ;
                             IF {}
                                { PUSH string "WrongCondition: sp.sender == self.data.administrator" ;
                                  FAILWITH } ;
                             DUP ;
                             CDR ;
                             DIG 2 ;
                             DUP ;
                             DUG 3 ;
                             CADR ;
                             DIG 2 ;
                             DUP ;
                             DUG 3 ;
                             CAR ;
                             GET ;
                             IF_SOME {} { PUSH int 70 ; FAILWITH } ;
                             CDR ;
                             COMPARE ;
                             GE ;
                             IF {}
                                { PUSH string
                                       "WrongCondition: self.data.balances[params.address].balance >= params.value" ;
                                  FAILWITH } ;
                             SWAP ;
                             DUP ;
                             DUG 2 ;
                             DUP ;
                             CDR ;
                             SWAP ;
                             CAR ;
                             DUP ;
                             CAR ;
                             SWAP ;
                             CDR ;
                             DUP ;
                             DIG 4 ;
                             DUP ;
                             DUG 5 ;
                             CAR ;
                             DUP ;
                             DUG 2 ;
                             GET ;
                             IF_SOME {} { PUSH int 71 ; FAILWITH } ;
                             CAR ;
                             DIG 5 ;
                             DUP ;
                             DUG 6 ;
                             CDR ;
                             DIG 7 ;
                             CADR ;
                             DIG 7 ;
                             DUP ;
                             DUG 8 ;
                             CAR ;
                             GET ;
                             IF_SOME {} { PUSH int 71 ; FAILWITH } ;
                             CDR ;
                             SUB ;
                             ISNAT ;
                             IF_SOME {} { PUSH int 71 ; FAILWITH } ;
                             SWAP ;
                             PAIR ;
                             SOME ;
                             SWAP ;
                             UPDATE ;
                             SWAP ;
                             PAIR ;
                             PAIR ;
                             DUP ;
                             DUG 2 ;
                             DUP ;
                             CAR ;
                             SWAP ;
                             CDAR ;
                             DIG 2 ;
                             CDR ;
                             DIG 3 ;
                             CDDR ;
                             SUB ;
                             ISNAT ;
                             IF_SOME {} { PUSH int 72 ; FAILWITH } ;
                             SWAP ;
                             PAIR ;
                             SWAP ;
                             PAIR } ;
                         NIL operation }
                       { IF_LEFT
                           { SWAP ;
                             DUP ;
                             DUG 2 ;
                             CAAR ;
                             NIL operation ;
                             DIG 2 ;
                             CDR ;
                             PUSH mutez 0 ;
                             DIG 3 ;
                             TRANSFER_TOKENS ;
                             CONS }
                           { IF_LEFT
                               { SWAP ;
                                 DUP ;
                                 DUG 2 ;
                                 CADR ;
                                 SWAP ;
                                 DUP ;
                                 DUG 2 ;
                                 CAAR ;
                                 GET ;
                                 IF_SOME {} { PUSH int 42 ; FAILWITH } ;
                                 CAR ;
                                 SWAP ;
                                 DUP ;
                                 DUG 2 ;
                                 CADR ;
                                 GET ;
                                 IF_SOME {} { PUSH int 42 ; FAILWITH } ;
                                 NIL operation ;
                                 DIG 2 ;
                                 CDR ;
                                 PUSH mutez 0 ;
                                 DIG 3 ;
                                 TRANSFER_TOKENS ;
                                 CONS }
                               { SWAP ;
                                 DUP ;
                                 DUG 2 ;
                                 CADR ;
                                 SWAP ;
                                 DUP ;
                                 DUG 2 ;
                                 CAR ;
                                 GET ;
                                 IF_SOME {} { PUSH int 38 ; FAILWITH } ;
                                 CDR ;
                                 NIL operation ;
                                 DIG 2 ;
                                 UNPAIR ;
                                 PUSH nat 1 ;
                                 SWAP ;
                                 TICKET ;
                                 DIG 3 ;
                                 SWAP ;
                                 PAIR ;
                                 PUSH mutez 0 ;
                                 SWAP ;
                                 TRANSFER_TOKENS ;
                                 CONS } } } }
                   { IF_LEFT
                       { IF_LEFT
                           { SWAP ;
                             DUP ;
                             DUG 2 ;
                             CDDR ;
                             NIL operation ;
                             DIG 2 ;
                             CDR ;
                             PUSH mutez 0 ;
                             DIG 3 ;
                             TRANSFER_TOKENS ;
                             CONS }
                           { SWAP ;
                             DUP ;
                             DUG 2 ;
                             CAAR ;
                             SENDER ;
                             COMPARE ;
                             EQ ;
                             IF {}
                                { PUSH string "WrongCondition: sp.sender == self.data.administrator" ;
                                  FAILWITH } ;
                             SWAP ;
                             DUP ;
                             DUG 2 ;
                             CADR ;
                             SWAP ;
                             DUP ;
                             DUG 2 ;
                             CAR ;
                             MEM ;
                             IF {}
                                { SWAP ;
                                  DUP ;
                                  CDR ;
                                  SWAP ;
                                  CAR ;
                                  DUP ;
                                  CAR ;
                                  SWAP ;
                                  CDR ;
                                  DIG 3 ;
                                  DUP ;
                                  DUG 4 ;
                                  CAR ;
                                  PUSH (option (pair (map %approvals address nat) (nat %balance))) (Some (Pair {} 0)) ;
                                  SWAP ;
                                  UPDATE ;
                                  SWAP ;
                                  PAIR ;
                                  PAIR ;
                                  SWAP } ;
                             SWAP ;
                             DUP ;
                             CDR ;
                             SWAP ;
                             CAR ;
                             DUP ;
                             CAR ;
                             SWAP ;
                             CDR ;
                             DUP ;
                             DIG 4 ;
                             DUP ;
                             DUG 5 ;
                             CAR ;
                             DUP ;
                             DUG 2 ;
                             GET ;
                             IF_SOME {} { PUSH int 63 ; FAILWITH } ;
                             DUP ;
                             CAR ;
                             SWAP ;
                             CDR ;
                             DIG 6 ;
                             DUP ;
                             DUG 7 ;
                             CDR ;
                             ADD ;
                             SWAP ;
                             PAIR ;
                             SOME ;
                             SWAP ;
                             UPDATE ;
                             SWAP ;
                             PAIR ;
                             PAIR ;
                             DUP ;
                             CAR ;
                             SWAP ;
                             CDR ;
                             DUP ;
                             CAR ;
                             SWAP ;
                             CDR ;
                             DIG 3 ;
                             CDR ;
                             ADD ;
                             SWAP ;
                             PAIR ;
                             SWAP ;
                             PAIR ;
                             NIL operation } }
                       { IF_LEFT
                           { SWAP ;
                             DUP ;
                             DUG 2 ;
                             CAAR ;
                             SENDER ;
                             COMPARE ;
                             EQ ;
                             IF {}
                                { PUSH string "WrongCondition: sp.sender == self.data.administrator" ;
                                  FAILWITH } ;
                             SWAP ;
                             DUP ;
                             CDR ;
                             SWAP ;
                             CADR ;
                             DIG 2 ;
                             PAIR ;
                             PAIR }
                           { IF_LEFT
                               { SWAP ;
                                 DUP ;
                                 DUG 2 ;
                                 CAAR ;
                                 SENDER ;
                                 COMPARE ;
                                 EQ ;
                                 IF {}
                                    { PUSH string "WrongCondition: sp.sender == self.data.administrator" ;
                                      FAILWITH } ;
                                 SWAP ;
                                 DUP ;
                                 CAR ;
                                 SWAP ;
                                 CDDR ;
                                 DIG 2 ;
                                 PAIR ;
                                 SWAP ;
                                 PAIR }
                               { SWAP ;
                                 DUP ;
                                 DUG 2 ;
                                 CAAR ;
                                 SENDER ;
                                 COMPARE ;
                                 EQ ;
                                 IF { PUSH bool True }
                                    { SWAP ;
                                      DUP ;
                                      DUG 2 ;
                                      CDAR ;
                                      IF { PUSH bool False }
                                         { DUP ;
                                           CAR ;
                                           SENDER ;
                                           COMPARE ;
                                           EQ ;
                                           IF { PUSH bool True }
                                              { DUP ;
                                                CDDR ;
                                                DIG 2 ;
                                                DUP ;
                                                DUG 3 ;
                                                CADR ;
                                                DIG 2 ;
                                                DUP ;
                                                DUG 3 ;
                                                CAR ;
                                                GET ;
                                                IF_SOME {} { PUSH int 13 ; FAILWITH } ;
                                                CAR ;
                                                SENDER ;
                                                GET ;
                                                IF_SOME {} { PUSH int 13 ; FAILWITH } ;
                                                COMPARE ;
                                                GE } } } ;
                                 IF {}
                                    { PUSH string
                                           "WrongCondition: (sp.sender == self.data.administrator) | ((~ self.data.paused) & ((params.from_ == sp.sender) | (self.data.balances[params.from_].approvals[sp.sender] >= params.value)))" ;
                                      FAILWITH } ;
                                 SWAP ;
                                 DUP ;
                                 DUG 2 ;
                                 CADR ;
                                 SWAP ;
                                 DUP ;
                                 DUG 2 ;
                                 CDAR ;
                                 MEM ;
                                 IF {}
                                    { SWAP ;
                                      DUP ;
                                      CDR ;
                                      SWAP ;
                                      CAR ;
                                      DUP ;
                                      CAR ;
                                      SWAP ;
                                      CDR ;
                                      DIG 3 ;
                                      DUP ;
                                      DUG 4 ;
                                      CDAR ;
                                      PUSH (option (pair (map %approvals address nat) (nat %balance))) (Some (Pair {} 0)) ;
                                      SWAP ;
                                      UPDATE ;
                                      SWAP ;
                                      PAIR ;
                                      PAIR ;
                                      SWAP } ;
                                 DUP ;
                                 CDDR ;
                                 DIG 2 ;
                                 DUP ;
                                 DUG 3 ;
                                 CADR ;
                                 DIG 2 ;
                                 DUP ;
                                 DUG 3 ;
                                 CAR ;
                                 GET ;
                                 IF_SOME {} { PUSH int 18 ; FAILWITH } ;
                                 CDR ;
                                 COMPARE ;
                                 GE ;
                                 IF {}
                                    { PUSH string
                                           "WrongCondition: self.data.balances[params.from_].balance >= params.value" ;
                                      FAILWITH } ;
                                 SWAP ;
                                 DUP ;
                                 DUG 2 ;
                                 DUP ;
                                 CDR ;
                                 SWAP ;
                                 CAR ;
                                 DUP ;
                                 CAR ;
                                 SWAP ;
                                 CDR ;
                                 DUP ;
                                 DIG 4 ;
                                 DUP ;
                                 DUG 5 ;
                                 CAR ;
                                 DUP ;
                                 DUG 2 ;
                                 GET ;
                                 IF_SOME {} { PUSH int 19 ; FAILWITH } ;
                                 CAR ;
                                 DIG 5 ;
                                 DUP ;
                                 DUG 6 ;
                                 CDDR ;
                                 DIG 7 ;
                                 CADR ;
                                 DIG 7 ;
                                 DUP ;
                                 DUG 8 ;
                                 CAR ;
                                 GET ;
                                 IF_SOME {} { PUSH int 19 ; FAILWITH } ;
                                 CDR ;
                                 SUB ;
                                 ISNAT ;
                                 IF_SOME {} { PUSH int 19 ; FAILWITH } ;
                                 SWAP ;
                                 PAIR ;
                                 SOME ;
                                 SWAP ;
                                 UPDATE ;
                                 SWAP ;
                                 PAIR ;
                                 PAIR ;
                                 DUP ;
                                 CDR ;
                                 SWAP ;
                                 CAR ;
                                 DUP ;
                                 CAR ;
                                 SWAP ;
                                 CDR ;
                                 DUP ;
                                 DIG 4 ;
                                 DUP ;
                                 DUG 5 ;
                                 CDAR ;
                                 DUP ;
                                 DUG 2 ;
                                 GET ;
                                 IF_SOME {} { PUSH int 20 ; FAILWITH } ;
                                 DUP ;
                                 CAR ;
                                 SWAP ;
                                 CDR ;
                                 DIG 6 ;
                                 DUP ;
                                 DUG 7 ;
                                 CDDR ;
                                 ADD ;
                                 SWAP ;
                                 PAIR ;
                                 SOME ;
                                 SWAP ;
                                 UPDATE ;
                                 SWAP ;
                                 PAIR ;
                                 PAIR ;
                                 SWAP ;
                                 DUP ;
                                 CAR ;
                                 SENDER ;
                                 COMPARE ;
                                 NEQ ;
                                 IF { SWAP ; DUP ; DUG 2 ; CAAR ; SENDER ; COMPARE ; NEQ }
                                    { PUSH bool False } ;
                                 IF { SWAP ;
                                      DUP ;
                                      DUG 2 ;
                                      DUP ;
                                      CDR ;
                                      SWAP ;
                                      CAR ;
                                      DUP ;
                                      CAR ;
                                      SWAP ;
                                      CDR ;
                                      DUP ;
                                      DIG 4 ;
                                      DUP ;
                                      DUG 5 ;
                                      CAR ;
                                      DUP ;
                                      DUG 2 ;
                                      GET ;
                                      IF_SOME {} { PUSH int 22 ; FAILWITH } ;
                                      DUP ;
                                      CDR ;
                                      SWAP ;
                                      CAR ;
                                      SENDER ;
                                      DIG 7 ;
                                      DUP ;
                                      DUG 8 ;
                                      CDDR ;
                                      DIG 9 ;
                                      CADR ;
                                      DIG 9 ;
                                      CAR ;
                                      GET ;
                                      IF_SOME {} { PUSH int 22 ; FAILWITH } ;
                                      CAR ;
                                      SENDER ;
                                      GET ;
                                      IF_SOME {} { PUSH int 22 ; FAILWITH } ;
                                      SUB ;
                                      ISNAT ;
                                      IF_SOME {} { PUSH int 22 ; FAILWITH } ;
                                      SOME ;
                                      SWAP ;
                                      UPDATE ;
                                      PAIR ;
                                      SOME ;
                                      SWAP ;
                                      UPDATE ;
                                      SWAP ;
                                      PAIR ;
                                      PAIR }
                                    { DROP } } } ;
                         NIL operation } } ;
                 PAIR } }
        Initial storage:
          (Pair (Pair "tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW" {}) (Pair False 0))
        No delegate for this contract
        This origination was successfully applied
        Originated contracts:
          KT1MPKu836t9AP6yeVE7rUm7faieYrpoKqWw
        Storage size: 3820 bytes
        Updated big_maps:
          New map(64) of type (big_map address (pair (map %approvals address nat) (nat %balance)))
        Paid storage size diff: 3820 bytes
        Consumed gas: 18496.784
        Balance updates:
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.955
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.06425

New contract KT1MPKu836t9AP6yeVE7rUm7faieYrpoKqWw originated.
The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for ooMsoty6HNztjafUJrkSPJYBskzxQwyeUvXJ9TWJSWJMFWxfLe6 to be included --confirmations 30 --branch BLai2f4AGoKv5YByBRUNndZVJsALNXBjBd9jKX2Z2ZzDvPmVcF6
and/or an external block explorer.
Contract memorized as cps-bank.
Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 2438.448 units (will add 100 for safety)
Estimated storage: 529 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'oobePVBE7bM4pxjkCkizLhARftuKasJ8WwGCUK2vJ8rUmQo2gNF'
Waiting for the operation to be included...
Operation found in block: BMDzqGyridaqHEdU4h4H8TrGQUbyJrp5XzPVQgWPZsgUGnNDRtF (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
    Fee to the baker: ꜩ0.000769
    Expected counter: 28436
    Gas limit: 2539
    Storage limit: 549 bytes
    Balance updates:
      tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ............ -ꜩ0.000769
      fees(tz1VWasoyFGAWZt5K2qZRzP3cWzv3z7MMhP8,12) ... +ꜩ0.000769
    Origination:
      From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
      Credit: ꜩ0
      Script:
        { parameter (pair %receive (ticket %auth address) (mutez %balance)) ;
          storage (pair (address %bank_address) (mutez %balance)) ;
          code { UNPAIR ;
                 UNPAIR ;
                 READ_TICKET ;
                 UNPAIR ;
                 DUP 5 ;
                 CAR ;
                 ASSERT_CMPEQ ;
                 UNPAIR ;
                 SELF_ADDRESS ;
                 ASSERT_CMPEQ ;
                 PUSH nat 1 ;
                 ASSERT_CMPEQ ;
                 DROP ;
                 UPDATE 2 ;
                 NIL operation ;
                 PAIR } }
        Initial storage: (Pair "KT1MPKu836t9AP6yeVE7rUm7faieYrpoKqWw" 0)
        No delegate for this contract
        This origination was successfully applied
        Originated contracts:
          KT1QHVhxUAUEYnL4yzzTKdsHSDci12E62VhP
        Storage size: 272 bytes
        Paid storage size diff: 272 bytes
        Consumed gas: 2438.448
        Balance updates:
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.068
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.06425

New contract KT1QHVhxUAUEYnL4yzzTKdsHSDci12E62VhP originated.
The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for oobePVBE7bM4pxjkCkizLhARftuKasJ8WwGCUK2vJ8rUmQo2gNF to be included --confirmations 30 --branch BLi1QNuRtT6H8em4HKnPqN6dcfYj6jJUBL69h1H2va5aFLrSEqP
and/or an external block explorer.
Contract memorized as cps-balance.
Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Error:
  Erroneous command line argument 7 (bootstrap1).
  no contract or key named bootstrap1
  bad contract notation
  Invalid contract notation "bootstrap1"

Usage:
  tezos-client [global options] command [command options]
  tezos-client --help (for global options)
  tezos-client [global options] command --help (for command options)

To browse the documentation:
  tezos-client [global options] man (for a list of commands)
  tezos-client [global options] man -v 3 (for the full manual)

Global options (must come before the command):
  -d --base-dir <path>: client data directory
  -c --config-file <path>: configuration file
  -t --timings: show RPC request times
  --chain <hash|tag>: chain on which to apply contextual commands (possible tags are 'main' and 'test')
  -b --block <hash|tag>: block on which to apply contextual commands (possible tags are 'head' and 'genesis')
  -w --wait <none|<int>>: how many confirmation blocks before to consider an operation as included
  -p --protocol <hash>: use commands of a specific protocol
  -l --log-requests: log all requests to the node
  -A --addr <IP addr|host>: [DEPRECATED: use --endpoint instead] IP address of the node
  -P --port <number>: [DEPRECATED: use --endpoint instead] RPC port of the node
  -S --tls: [DEPRECATED: use --endpoint instead] use TLS to connect to node.
  -E --endpoint <uri>: HTTP(S) endpoint of the node RPC interface; e.g. 'http://localhost:8732'
  -R --remote-signer <uri>: URI of the remote signer
  -f --password-filename <filename>: path to the password filename
  -M --mode <client|mockup>: how to interact with the node
Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 2286.371 units (will add 100 for safety)
Estimated storage: 480 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'op8AipsT8DBzUr6Te5hiahwe91FCEVdZ9Q5CqBysxF18fT35GuG'
Waiting for the operation to be included...
Operation found in block: BLrmUvAs4cdwt8avrSYo9X6WJD1oAGGYnmsR8LhCJzQsmPPUfx2 (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
    Fee to the baker: ꜩ0.000691
    Expected counter: 28437
    Gas limit: 2387
    Storage limit: 500 bytes
    Balance updates:
      tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ............ -ꜩ0.000691
      fees(tz3Q67aMz7gSMiQRcW729sXSfuMtkyAHYfqc,12) ... +ꜩ0.000691
    Origination:
      From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
      Credit: ꜩ0
      Script:
        { parameter
            (or (pair %sendConvertedBalance (ticket address) nat) (mutez %setConversionRate)) ;
          storage mutez ;
          code { UNPAIR ;
                 IF_LEFT
                   { UNPAIR ;
                     READ_TICKET ;
                     CDAR ;
                     CONTRACT (pair (ticket address) mutez) ;
                     IF_NONE
                       { DROP ; PUSH string "contract not found" ; FAILWITH }
                       { PUSH mutez 0 ;
                         DIP 3 { DUP 2 ; MUL } ;
                         DIP 2 { PAIR } ;
                         DIG 2 ;
                         TRANSFER_TOKENS } ;
                     NIL operation ;
                     SWAP ;
                     CONS }
                   { SWAP ; DROP ; NIL operation } ;
                 PAIR } }
        Initial storage: 2
        No delegate for this contract
        This origination was successfully applied
        Originated contracts:
          KT1D7MfG9CEBav7TXsa4xbPL3QZgR5eEgx7g
        Storage size: 223 bytes
        Paid storage size diff: 223 bytes
        Consumed gas: 2286.371
        Balance updates:
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.05575
          tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.06425

New contract KT1D7MfG9CEBav7TXsa4xbPL3QZgR5eEgx7g originated.
The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for op8AipsT8DBzUr6Te5hiahwe91FCEVdZ9Q5CqBysxF18fT35GuG to be included --confirmations 30 --branch BMWaGPVsJn7ydxy2KAKcnUriNew5nmQtiHArTpqwjRLqevKH2oS
and/or an external block explorer.
Contract memorized as cps-oracle.
Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 20123.527 units (will add 100 for safety)
Estimated storage: 74 bytes added (will add 20 for safety)
Operation successfully injected in the node.
Operation hash is 'onyAdbHctXbzUtVnZqfRHQMChZm8MoRyqenxeB3bWEH2xj9jQbv'
Waiting for the operation to be included...
Operation found in block: BKt7R8Nz1WYrvcqcKZRqJ7MAtkgjHttHaBkEdT2UmvMa3r8CL2d (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
    Fee to the baker: ꜩ0.002329
    Expected counter: 28438
    Gas limit: 20224
    Storage limit: 94 bytes
    Balance updates:
      tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ............ -ꜩ0.002329
      fees(tz1cXeGHP8Urj2pQRwpAkCdPGbCdqFUPsQwU,12) ... +ꜩ0.002329
    Transaction:
      Amount: ꜩ0
      From: tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW
      To: KT1MPKu836t9AP6yeVE7rUm7faieYrpoKqWw
      Entrypoint: mint
      Parameter: (Pair "KT1QHVhxUAUEYnL4yzzTKdsHSDci12E62VhP" 12)
      This transaction was successfully applied
      Updated storage:
        (Pair (Pair 0x000008093363b0d4ddfbbcd73f2c7747e4a0fb3a36e4 64) (Pair False 12))
      Updated big_maps:
        Set map(64)[0x01ac3db3f54a0e265474ccd3b90abadc4b2753794400] to (Pair {} 12)
      Storage size: 3894 bytes
      Paid storage size diff: 74 bytes
      Consumed gas: 20123.527
      Balance updates:
        tz1LNX7w32LntUkXcdQe1qyvFSTgwtYAqnGW ... -ꜩ0.0185

The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for onyAdbHctXbzUtVnZqfRHQMChZm8MoRyqenxeB3bWEH2xj9jQbv to be included --confirmations 30 --branch BLRahc4tDGVXEbqWLBLubpVVumYdz8r1bBkp2BDj8N9WmPMpeMv
and/or an external block explorer.
Warning:  the --addr --port --tls options are now deprecated; use --endpoint instead
Node is bootstrapped.
Estimated gas: 30290.248 units (will add 100 for safety)
Estimated storage: no bytes added
Operation successfully injected in the node.
Operation hash is 'oo2qTCeotXN8EXTLoaiee3Hg6ahUbAcWztX8JgxTXChmwyD3xb8'
Waiting for the operation to be included...
Operation found in block: BLzmVeqrLub4NUueEuMzGbTJf1Q1MgfVhJFGTgRZzX7dMH5oN3h (pass: 3, offset: 0)
This sequence of operations was run:
  Manager signed operations:
    From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
    Fee to the baker: ꜩ0.003412
    Expected counter: 28437
    Gas limit: 30391
    Storage limit: 0 bytes
    Balance updates:
      tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv ............ -ꜩ0.003412
      fees(tz3Q67aMz7gSMiQRcW729sXSfuMtkyAHYfqc,12) ... +ꜩ0.003412
    Transaction:
      Amount: ꜩ0
      From: tz1VeDGbCBNECVML7s7vkTQGSUCtSE54ZGAv
      To: KT1MPKu836t9AP6yeVE7rUm7faieYrpoKqWw
      Entrypoint: getBalance
      Parameter: (Pair "KT1QHVhxUAUEYnL4yzzTKdsHSDci12E62VhP"
                       "KT1D7MfG9CEBav7TXsa4xbPL3QZgR5eEgx7g%sendConvertedBalance")
      This transaction was successfully applied
      Updated storage:
        (Pair (Pair 0x000008093363b0d4ddfbbcd73f2c7747e4a0fb3a36e4 64) (Pair False 12))
      Storage size: 3894 bytes
      Consumed gas: 21721.468
    Internal operations:
      Transaction:
        Amount: ꜩ0
        From: KT1MPKu836t9AP6yeVE7rUm7faieYrpoKqWw
        To: KT1D7MfG9CEBav7TXsa4xbPL3QZgR5eEgx7g
        Entrypoint: sendConvertedBalance
        Parameter: (Pair (Pair 0x018c6fa26e0cee836972a45d4531c423b6f3bbdfb000
                               (Pair 0x01ac3db3f54a0e265474ccd3b90abadc4b2753794400 1))
                         12)
        This transaction was successfully applied
        Updated storage: 2
        Storage size: 223 bytes
        Consumed gas: 4981.727
      Transaction:
        Amount: ꜩ0
        From: KT1D7MfG9CEBav7TXsa4xbPL3QZgR5eEgx7g
        To: KT1QHVhxUAUEYnL4yzzTKdsHSDci12E62VhP
        Parameter: (Pair (Pair 0x018c6fa26e0cee836972a45d4531c423b6f3bbdfb000
                               (Pair 0x01ac3db3f54a0e265474ccd3b90abadc4b2753794400 1))
                         24)
        This transaction was successfully applied
        Updated storage:
          (Pair 0x018c6fa26e0cee836972a45d4531c423b6f3bbdfb000 24)
        Storage size: 272 bytes
        Consumed gas: 3587.053

The operation has only been included 0 blocks ago.
We recommend to wait more.
Use command
  tezos-client wait for oo2qTCeotXN8EXTLoaiee3Hg6ahUbAcWztX8JgxTXChmwyD3xb8 to be included --confirmations 30 --branch BLNnbrLMxt5mVfCodpQunmAeYwM9ib1gcJtoT8f85zPXW51RX5U
and/or an external block explorer.
