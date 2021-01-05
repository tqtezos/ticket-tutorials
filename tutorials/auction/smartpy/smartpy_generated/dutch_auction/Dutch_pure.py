import smartpy as sp

AUCTION_PARAMS_TYPE = sp.TRecord(opening_price = sp.TNat,
        reserve_price = sp.TNat,
        start_time = sp.TTimestamp,
        round_time = sp.TInt,
        ticket = sp.TTicket(sp.TNat))

METADATA_TYPE = sp.TMap(sp.TString, sp.TBytes)

TOKEN_METADATA_TYPE = sp.TBigMap(sp.TNat,
        sp.TPair(sp.TNat, METADATA_TYPE))

class NFTWallet(sp.Contract):
    def __init__(self, owner):
        self.add_flag("edo")
        self.init_type(sp.TRecord(admin = sp.TAddress,
                 tickets = sp.TBigMap(sp.TNat,
                   sp.TTicket(sp.TNat)),
                 current_id = sp.TNat,
                 token_metadata = TOKEN_METADATA_TYPE))
        self.init(admin = owner,
                tickets = sp.big_map({}),
                current_id = 0,
                token_metadata = sp.big_map({}))

    @sp.entry_point
    def createNft(self, metadata):
        sp.set_type(metadata, METADATA_TYPE)
        sp.verify(sp.sender == self.data.admin)
        my_ticket = sp.ticket(self.data.current_id, 1)
        current_id = self.data.current_id
        new_map = sp.update_map(self.data.tickets, current_id, sp.some(my_ticket))
        self.data.tickets = new_map
        self.data.token_metadata[current_id] = sp.pair(current_id, metadata)
        self.data.current_id = current_id + 1

    @sp.entry_point
    def receiveNft(self, nft):
        sp.set_type(nft, sp.TTicket(sp.TNat))
        ticket_data, ticket_next = sp.read_ticket(nft)
        qty = sp.compute(sp.snd(sp.snd(ticket_data)))
        originator = sp.compute(sp.fst(ticket_data))
        id = sp.compute(sp.fst(sp.snd(ticket_data)))
        sp.verify(qty == 1, "Only send 1 Nft to this entrypoint")
        sp.verify(sp.source == self.data.admin, "Ticket needs to be sent by wallet admin")
        current_id = self.data.current_id
        new_map = sp.update_map(self.data.tickets, current_id, sp.some(ticket_next))
        self.data.tickets = new_map
        self.data.current_id = current_id + 1

    @sp.entry_point
    def sendNft(self, params):
        sp.set_type(params, sp.TRecord(ticket_id = sp.TNat, send_to = sp.TContract(sp.TTicket(sp.TNat))))
        sp.verify(sp.sender == self.data.admin)
        my_ticket, new_map = sp.get_and_update(self.data.tickets, params.ticket_id, sp.none)
        sp.verify(my_ticket.is_some(), "Ticket does not exist")

        self.data.tickets = new_map
        sp.transfer(my_ticket.open_some(), sp.mutez(0), params.send_to)

    @sp.entry_point
    def configNftAuction(self, params):
        sp.verify(sp.sender == self.data.admin)
        sp.set_type(params, sp.TRecord(auction_address = sp.TAddress,
                opening_price = sp.TNat,
                reserve_price = sp.TNat,
                start_time = sp.TTimestamp,
                round_time = sp.TInt,
                ticket_id = sp.TNat))
        my_ticket, new_map = sp.get_and_update(self.data.tickets, params.ticket_id, sp.none)
        sp.verify(my_ticket.is_some(), "Ticket does not exist")
        self.data.tickets = new_map
        auction_params = sp.record(opening_price = params.opening_price,
                reserve_price = params.reserve_price,
                start_time = params.start_time,
                round_time = params.round_time,
                ticket = my_ticket.open_some())
        auction_contract = sp.contract(AUCTION_PARAMS_TYPE, params.auction_address, entry_point = "configureAuction").open_some()
        sp.transfer(auction_params, sp.mutez(0), auction_contract)

class DutchAuction(sp.Contract):
    def __init__(self, admin):
        self.add_flag("edo")
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
                ticket = sp.TOption(sp.TTicket(sp.TNat))))

    @sp.entry_point
    def configureAuction(self, params):
        sp.set_type(params, AUCTION_PARAMS_TYPE)
        sp.verify(sp.source == self.data.owner, "User Not Authorized")
        sp.verify(~self.data.in_progress, "Auction in progress")

        self.data.current_price = params.opening_price
        self.data.reserve_price = params.reserve_price
        self.data.start_time = params.start_time
        self.data.round_time = params.round_time
        self.data.ticket = sp.some(params.ticket)

    @sp.entry_point
    def startAuction(self):
        sp.verify(sp.sender == self.data.owner, "User not Authorized")
        sp.verify(~self.data.in_progress, "Auction in progress")
        #Verify ticket/asset sent
        sp.verify(self.data.ticket.is_some(), "No ticket to auction")
        # verify now is at least start time of auction
        sp.verify(sp.now >= self.data.start_time, "Too early to start auction")

        self.data.in_progress = sp.bool(True)
        self.data.start_time = sp.now

    @sp.entry_point
    def dropPrice(self, new_price):
        sp.set_type(new_price, sp.TNat)
        sp.verify(sp.sender == self.data.owner, "User not Authorized")
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
        c = sp.contract(sp.TTicket(sp.TNat), wallet_address, entry_point = "receiveNft").open_some()
        sp.transfer(self.data.ticket.open_some(), sp.mutez(0), c)

        # endAuction
        self.data.ticket = sp.none
        self.data.in_progress = sp.bool(False)

    @sp.entry_point
    def cancelAuction(self):
        sp.verify(self.data.in_progress, "No Auction in progress")
        sp.verify(sp.sender == self.data.owner, "User not Authorized")
        self.data.current_price = 0

        #Send back ticket to owner
        c = sp.contract(sp.TTicket(sp.TNat), self.data.owner, entry_point = "receiveNft").open_some()
        sp.transfer(self.data.ticket.open_some(), sp.mutez(0), c)
        # endAuction
        self.data.ticket = sp.none
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

    alice_wallet = NFTWallet(alice.address)
    bob_wallet = NFTWallet(bob.address)

    scenario += alice_wallet
    scenario += bob_wallet

    scenario.h2("Create NFT")

    token_metadata = sp.map({"name" : sp.bytes_of_string("Nft1")})
    scenario += alice_wallet.createNft(token_metadata).run(sender = alice)

    scenario.h2("Configure and start auction")
    scenario += alice_wallet.configNftAuction(auction_address = auction.address,
            opening_price = 100,
            reserve_price = 10,
            start_time = time,
            round_time = 1000,
            ticket_id = 0).run(source = alice, sender = alice, now = time)
    scenario.verify(~ alice_wallet.data.tickets.contains(0))
    time = time.add_seconds(1)
    scenario += auction.startAuction().run(sender = alice, now = time)

    time = time.add_seconds(6001)

    scenario += auction.dropPrice(90).run(sender = alice, now = time)

    scenario.h2("Bob buys")
    time = time.add_seconds(1)
    scenario += auction.buy(bob_wallet.address).run(sender = bob, source = bob, now = time, amount = sp.mutez(90))
    scenario.verify(bob_wallet.data.tickets.contains(0))
    scenario.verify(~ auction.data.ticket.is_some())

