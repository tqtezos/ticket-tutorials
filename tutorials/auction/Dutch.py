#Based on contract at https://github.com/muditmarda/TezAuction/blob/master/contracts/Dutch.py

import smartpy as sp

auction_params_type = sp.TRecord(opening_price = sp.TNat,
        reserve_price = sp.TNat,
        start_time = sp.TTimestamp,
        round_time = sp.TInt,
        ticket = sp.TTicket(sp.TString))

class NFTWallet(sp.Contract):
    def __init__(self, owner):
        self.init_type(sp.TRecord(admin = sp.TAddress,
                 tickets = sp.TBigMap(sp.TString,
                 sp.TPair(sp.TOption(sp.TTicket(sp.TString)),
                 sp.TOption(sp.TBytes)))))
        self.init(admin = owner,
                tickets = sp.big_map(tkey = sp.TString,
                tvalue = sp.TPair(sp.TOption(sp.TTicket(sp.TString)),
                sp.TOption(sp.TBytes))))

    @sp.entry_point
    def createNft(self, params):
        sp.set_type(params, sp.TRecord(name = sp.TString, metadata = sp.TBytes))
        sp.verify(sp.sender == self.data.admin)
        t = sp.ticket(params.name, 1)
        self.data.tickets[params.name] = sp.pair(sp.some(t), sp.some(params.metadata))

    @sp.entry_point
    def receiveNft(self, nft):
        sp.set_type(nft, sp.TTicket(sp.TString))
        ticket_data, ticket_next = sp.read_ticket(nft)
        qty = sp.compute(sp.snd(sp.snd(ticket_data)))
        originator = sp.compute(sp.fst(ticket_data))
        name = sp.compute(sp.fst(sp.snd(ticket_data)))
        sp.verify(~ (self.data.tickets.contains(name) & sp.fst(self.data.tickets[name]).is_some()), "Duplicate Ticket")
        sp.verify(qty == 1, "Only send 1 Nft to this entrypoint")
        sp.verify(sp.source == self.data.admin, "Ticket needs to be sent by wallet admin")

        self.data.tickets[name] = sp.pair(sp.some(ticket_next), sp.none)

    def sendNft(self, params):
        sp.set_type(params, sp.TRecord(ticket_name = sp.TString, send_to = sp.TContract(sp.TTicket(sp.TString))))
        sp.verify(sp.sender == self.data.admin)
        sp.verify(self.data.tickets.contains(params.ticket_name) & sp.fst(self.data.tickets[params.ticket_name]).is_some(), "Ticket does not exist")
        t = self.data.tickets[params.ticket_name].open_some()
        sp.transfer(t, sp.mutez(0), c)

    @sp.entry_point
    def getNftData(self, params):
        params_type = sp.TPair(sp.TString, sp.TContract(sp.TBytes))
        sp.set_type(params, params_type)
        ticket_name = sp.fst(params)
        requesting_contract = sp.snd(params)
        sp.verify(self.data.tickets.contains(ticket_name) & sp.fst(self.data.tickets[ticket_name]).is_some(), "Ticket does not exist")
        ticket = sp.fst(self.data.tickets[ticket_name]).open_some()
        possible_metadata = sp.snd(self.data.tickets[ticket_name])
        sp.if possible_metadata.is_some():
          sp.transfer(possible_metadata.open_some(), sp.mutez(0), requesting_contract)
        sp.else:
          ticket_address = sp.compute(sp.fst(sp.fst(sp.read_ticket(ticket))))
          c = sp.contract(params_type, ticket_address, entry_point = "getNftData").open_some()
          sp.transfer(params, sp.mutez(0), c)

    @sp.entry_point
    def configNftAuction(self, params):
        sp.verify(sp.sender == self.data.admin)
        sp.set_type(params, sp.TRecord(auction_address = sp.TAddress,
                opening_price = sp.TNat,
                reserve_price = sp.TNat,
                start_time = sp.TTimestamp,
                round_time = sp.TInt,
                ticket_name = sp.TString))
        sp.verify(self.data.tickets.contains(params.ticket_name) & sp.fst(self.data.tickets[params.ticket_name]).is_some(), "Ticket does not exist")
        auction_params = sp.record(opening_price = params.opening_price,
                reserve_price = params.reserve_price,
                start_time = params.start_time,
                round_time = params.round_time,
                ticket = sp.fst(self.data.tickets[params.ticket_name]).open_some())
        auction_contract = sp.contract(auction_params_type, params.auction_address, entry_point = "configureAuction").open_some()
        sp.transfer(auction_params, sp.mutez(0), auction_contract)

    @sp.entry_point
    def startNftAuction(self, auction_address):
        sp.verify(sp.sender == self.data.admin)
        auction_contract = sp.contract(sp.TUnit, auction_address, entry_point = "startAuction").open_some()
        sp.transfer(sp.unit, sp.mutez(0), auction_contract)

class DutchAuction(sp.Contract):
    def __init__(self, admin):
        self.init(owner = admin,
                current_price = 0,
                reserve_price = 0,
                in_progress = sp.bool(False),
                start_time = sp.timestamp(0),
                round_time = 0,
                ticket = sp.none)
        self.init_type(t = sp.TRecord(owner = sp.TAddress,
                current_price = sp.TNat,
                reserve_price = sp.TNat,
                in_progress = sp.TBool,
                start_time = sp.TTimestamp,
                round_time = sp.TInt,
                ticket = sp.TOption(sp.TTicket(sp.TString))))

    @sp.entry_point
    def configureAuction(self, params):
        sp.set_type(params, auction_params_type)
        sp.verify(sp.sender == self.data.owner, "User Not Authorized")
        sp.verify(~self.data.in_progress, "Auction in progress")

        self.data.current_price = params.opening_price
        self.data.reserve_price = params.reserve_price
        self.data.start_time = params.start_time
        self.data.round_time = params.round_time
        self.data.ticket = sp.some(params.ticket)

    @sp.entry_point
    def startAuction(self):
        sp.verify(sp.sender == self.data.owner)
        sp.verify(~self.data.in_progress)
        #Verify ticket/asset sent
        sp.verify(self.data.ticket.is_some())
        # verify now is less than round_end_time = start_time + round_time
        sp.verify(sp.now < self.data.start_time.add_seconds(self.data.round_time))

        self.data.in_progress = sp.bool(True)
        self.data.start_time = sp.now

    @sp.entry_point
    def dropPrice(self, new_price):
        sp.set_type(new_price, sp.TNat)
        sp.verify(sp.sender == self.data.owner, "User Not Authorized")
        sp.verify(self.data.in_progress, "No Auction in progress")
        sp.verify(new_price < self.data.current_price, "Price not dropped")
        sp.verify(new_price >= self.data.reserve_price, "Price below reserve_price")
        # verify now more than round_end_time = start_time + round_time
        sp.verify(sp.now > self.data.start_time.add_seconds(self.data.round_time), "Previous round has not ended")

        self.data.current_price = new_price
        self.data.start_time = sp.now

    @sp.entry_point
    def buy(self, wallet_address):
        sp.set_type(wallet_address, sp.TAddress)
        sp.verify(self.data.in_progress)
        sp.verify(~(sp.sender == self.data.owner))
        sp.verify(sp.amount == sp.mutez(self.data.current_price))
        # verify now less than round_end_time = start_time + round_time
        sp.verify(sp.now < self.data.start_time.add_seconds(self.data.round_time))

        sp.send(self.data.owner, sp.amount)

        #Send ticket/asset to winner. They must have a "receive_ticket" entrypoint that accepts ticket of correct type
        c = sp.contract(sp.TTicket(sp.TString), wallet_address, entry_point = "receiveNft").open_some()
        sp.transfer(self.data.ticket.open_some(), sp.mutez(0), c)

        # endAuction
        #Do I need to set to none?
        #self.data.ticket = sp.none
        self.data.in_progress = sp.bool(False)

    @sp.entry_point
    def cancelAuction(self, params):
        sp.verify(self.data.in_progress)
        sp.verify(sp.sender == self.data.owner)
        self.data.current_price = 0

        #Send back ticket to owner
        c = sp.contract(sp.TTicket(sp.TString), self.data.owner, entry_point = "receiveNft").open_some()
        sp.transfer(self.data.ticket.open_some(), sp.mutez(0), c)
        # endAuction
        #Do I need to set to none?
        #self.data.ticket = sp.none
        self.data.in_progress = sp.bool(False)

class Viewer(sp.Contract):
    def __init__(self, t):
        self.init(last = sp.none)
        self.init_type(sp.TRecord(last = sp.TOption(t)))
    @sp.entry_point
    def target(self, params):
        self.data.last = sp.some(params)

@sp.add_test(name = "Test Auction")
def test():
    time = sp.timestamp(1571761674)
    # Create test scenario
    scenario = sp.test_scenario()

    scenario.table_of_contents()

    # sp.test_account generates ED25519 key-pairs deterministically:
    alice = sp.test_account("Alice")
    bob = sp.test_account("Robert")

    # Create HTML output for debugging
    scenario.h1("Dutch Auction")

    # Instantiate Auction contract
    auction = DutchAuction(alice.address)
    scenario += auction

    #alice_wallet = NFTWallet(alice.address)
    #t = sp.test_ticket(alice_wallet, "nft1", 1)
#
    #scenario += auction.configureAuction(current_price = 100,
    #        reserve_price = 10,
    #        start_time = time,
    #        round_time = 6000,
    #        ticket = t).run(sender = alice_wallet)

    #scenario += auction.startAuction().run(sender = alice)
#
    #new_time = time.add_seconds(6001)
#
    #scenario += auction.dropPrice(new_price = 90).run(sender = bob, now = new_time)

    #alice_wallet = NFTWallet(alice.address)
    #bob_wallet = NFTWallet(bob.address)
    #scenario += alice_wallet
    #scenario += bob_wallet
#
    #scenario.h2("Create NFT")
#
    #scenario += alice_wallet.createNft(name = "nft1", metadata = sp.bytes('0x0000')).run(sender = alice)
#
    #scenario.h2("Configure and start auction")
    #scenario += alice_wallet.configNftAuction(auction_address = auction.address,
    #        opening_price = 100,
    #        reserve_price = 10,
    #        start_time = time,
    #        round_time = 1000,
    #        ticket_name = "nft1").run(sender = alice, now = time)
    #scenario.verify(~ alice_wallet.data.tickets.contains("nft1"))
    #time = time.add_seconds(1)
    #scenario += alice_wallet.startNftAuction(auction.address).run(sender = alice, now = time)
#
    #scenario.h2("Bob buys")
    #time = time.add_seconds(1)
    #scenario += auction.buy(bob_wallet.address).run(sender = bob, now = time)
    #scenario.verify(bob_wallet.data.tickets.contains("nft1"))
    #scenario.verify(~ auction.data.ticket.is_some())