#Based on contract at https://github.com/muditmarda/TezAuction/blob/master/contracts/Dutch.py

import smartpy as sp

# An Oracle is the on-chain incarnation of an Oracle provider
# It maintains a queue of requests of type request_type containing an amount
# paid, a sender, an entry_point and a list of parameters.

# Parameters of type parameters_type is a list of (name, dict) pairs.

value_type = sp.TVariant(int = sp.TInt, string = sp.TString, bytes = sp.TBytes)

def value_string(s):
    return sp.variant("string", s)

def value_bytes(s):
    return sp.variant("bytes", s)

def value_int(s):
    return sp.variant("int", s)

wLINK_decimals = 1000000000000000000

# Request parameters
parameters_type = sp.TMap(sp.TString, value_type)

# Full request specification type
request_type = sp.TRecord(amount            = sp.TNat,
                          target            = sp.TAddress,
                          job_id            = sp.TBytes,
                          parameters        = parameters_type,
                          timeout           = sp.TTimestamp,
                          client_request_id = sp.TNat)

# A Client is a smart contract that expects to be called by oracles.
# The simplest form of a Client contains a receive entry point (custom
# names are possible) with an arbitrary parameter type and expects to
# be called by the operator of an oracle called oracle_admin.

class Client_requester():
    def request_helper(self, amount, job_id, parameters, oracle, waiting_request_id, target, timeout_minutes = 5):
        parameters = sp.set_type_expr(parameters, parameters_type)
        sp.verify(~ waiting_request_id.is_some(), message = "Request pending")
        target = sp.set_type_expr(target, sp.TContract(sp.TRecord(client_request_id = sp.TNat, result = value_type)))
        waiting_request_id.set(sp.some(self.data.next_request_id))
        token  = sp.contract(sp.TRecord(oracle = sp.TAddress, params = request_type), self.data.token, entry_point = "proxy").open_some(message = "Incompatible token interface")
        params = sp.record(amount        = amount,
                           target        = sp.to_address(target),
                           job_id        = job_id,
                           parameters    = parameters,
                           timeout       = sp.now.add_minutes(timeout_minutes),
                           client_request_id = self.data.next_request_id)
        sp.transfer(sp.record(oracle = oracle, params = params), sp.mutez(0), token)
        self.data.next_request_id += 1

    def cancel_helper(self, oracle, waiting_request_id):
        sp.verify(waiting_request_id.is_some(), message = "No pending request")
        oracle_contract = sp.contract(sp.TNat, oracle, entry_point = "cancel_request").open_some(message = "Incompatible oracle interface")
        sp.transfer(waiting_request_id.open_some(), sp.mutez(0), oracle_contract)
        waiting_request_id.set(sp.none)

class Client_receiver():
    def check_receive(self, oracle, client_request_id, waiting_request_id, result):
        sp.verify(sp.sender == oracle, message = "Invalid source")
        sp.verify(waiting_request_id.is_some() & (waiting_request_id.open_some() == client_request_id), message = "Response mismatch")
        waiting_request_id.set(sp.none)
        sp.set_type(client_request_id, sp.TNat)
        sp.set_type(result, value_type)

    def read_int(self, x):
        return x.open_variant("int")

    def read_bytes(self, x):
        return x.open_variant("bytes")

    def read_string(self, x):
        return x.open_variant("string")

class DutchAuctionFactory(sp.Contract):
    def __init__(self, master_auction_contract, owner):
        self.dutch = DutchAuction()
        self.init(
            master_auction_contract = master_auction_contract,
            owner = owner,

            # Oracle specific
            oracle = sp.address("KT1JWENqDEoGasUty7m22QBPk6gfau8H4VQS"),
            link_token = sp.address("KT1TQR3eyYCytqBK9EB28J1taa2cX41F9R8x"),
            oracle_job_id = sp.bytes('0x67')
        )

    @sp.entry_point
    def setMasterAuctionContractAddress(self, master_auction_contract):
        sp.verify(sp.sender == self.data.owner)
        self.data.master_auction_contract = master_auction_contract

    @sp.entry_point
    def createDutchAuctionInstance(self, asset_id):
        sp.verify(sp.sender == self.data.master_auction_contract)

        contract_address = sp.some(sp.create_contract(
            storage = sp.record(owner = sp.source,
                master_auction_contract = self.data.master_auction_contract,
                asset_id = asset_id,
                current_price = 0,
                reserve_price = 0,
                started = sp.bool(False),
                ended = sp.bool(False),
                start_time = sp.now,
                round_time = 0,

                oracle = self.data.oracle,
                token = self.data.link_token,
                next_request_id = 1,
                waiting_request_id = sp.none,
                oracle_job_id = self.data.oracle_job_id),
            contract = self.dutch))

        # registerInstance
        c = sp.contract(sp.TRecord(asset_id = sp.TNat, contract_address = sp.TAddress),  self.data.master_auction_contract, entry_point = "registerInstance").open_some()
        sp.transfer(sp.record(asset_id = asset_id, contract_address = contract_address.open_some()), sp.mutez(0), c)



class DutchAuction(sp.Contract, Client_requester, Client_receiver):
    def __init__(self):
        self.init_type(t = sp.TRecord(owner = sp.TAddress,
                master_auction_contract = sp.TAddress,
                asset_id = sp.TNat,
                current_price = sp.TNat,
                reserve_price = sp.TNat,
                started = sp.TBool,
                ended = sp.TBool,
                start_time = sp.TTimestamp,
                round_time = sp.TInt,

                oracle = sp.TAddress,
                token = sp.TAddress,
                next_request_id = sp.TNat,
                waiting_request_id = sp.TOption(sp.TNat),
                oracle_job_id = sp.TBytes))
                # round_time (gets refreshed for each bid)

    @sp.entry_point
    def configureAuction(self, params):
        sp.verify(sp.sender == self.data.owner)
        sp.verify(~self.data.started)
        sp.verify(~self.data.ended)

        self.data.current_price = params.opening_price
        self.data.reserve_price = params.reserve_price
        self.data.start_time = params.start_time
        self.data.round_time = params.round_time

        # configureInstance
        c = sp.contract(sp.TNat, self.data.master_auction_contract, entry_point = "configureInstance").open_some()
        sp.transfer(self.data.asset_id, sp.mutez(0), c)

    @sp.entry_point
    def startAuction(self, params):
        sp.verify(sp.sender == self.data.owner)
        sp.verify(~self.data.started)
        sp.verify(~self.data.ended)
        # verify now is less than round_end_time = start_time + round_time
        sp.verify(sp.now < self.data.start_time.add_seconds(self.data.round_time))

        self.data.started = sp.bool(True)
        self.data.start_time = sp.now

        # startedAuction
        c = sp.contract(sp.TNat, self.data.master_auction_contract, entry_point = "startedAuction").open_some()
        sp.transfer(self.data.asset_id, sp.mutez(0), c)


    @sp.entry_point
    def dropPrice(self, params):
        sp.verify(sp.sender == self.data.owner)
        sp.verify(self.data.started)
        sp.verify(~self.data.ended)
        sp.verify(params.new_price < self.data.current_price)
        sp.verify(params.new_price >= self.data.reserve_price)
        # verify now more than round_end_time = start_time + round_time
        sp.verify(sp.now > self.data.start_time.add_seconds(self.data.round_time))

        self.data.current_price = params.new_price
        self.data.start_time = sp.now

    @sp.entry_point
    def callback(self, client_request_id, result):
        self.check_receive(
            self.data.oracle,
            client_request_id,
            self.data.waiting_request_id,
            result)

        sp.verify_equal(self.read_string(result), "DELIVERED")
        self.acceptPrice()
        self.data.waiting_request_id = sp.none

    @sp.entry_point
    def requestTrackInfo(self, params):
        self.request_helper(
            params.payment,
            self.data.oracle_job_id,
            params.parameters,
            self.data.oracle,
            self.data.waiting_request_id,
            sp.self_entry_point("callback"),
            params.timeout)

    @sp.entry_point
    def cancelTrackRequest(self):
        self.cancel_helper(self.data.oracle, self.data.waiting_request_id)

    def acceptPrice(self):
        sp.verify(self.data.started)
        sp.verify(~self.data.ended)
        sp.verify(~(sp.sender == self.data.owner))
        sp.verify(sp.amount == sp.mutez(self.data.current_price))
        # verify now less than round_end_time = start_time + round_time
        sp.verify(sp.now < self.data.start_time.add_seconds(self.data.round_time))

        sp.send(self.data.owner, sp.amount)

        self.data.owner = sp.sender

        # endAuction
        self.endAuction(self.data.asset_id, self.data.owner)

    @sp.entry_point
    def cancelAuction(self, params):
        sp.verify(self.data.started)
        sp.verify(~self.data.ended)
        sp.verify(sp.sender == self.data.owner)

        self.data.current_price = 0

        # endAuction
        self.endAuction(self.data.asset_id, self.data.owner)

    def endAuction(self, asset_id, owner):
        self.data.ended = sp.bool(True)

        # destroyInstance
        c = sp.contract(sp.TRecord(asset_id = sp.TNat, owner = sp.TAddress), self.data.master_auction_contract, entry_point = "destroyInstance").open_some()
        sp.transfer(sp.record(asset_id = asset_id, owner = owner), sp.mutez(0), c)



@sp.add_test(name = "Test Auction")
def test():
    # Create test scenario
    scenario = sp.test_scenario()

    # Create HTML output for debugging
    scenario.h1("Dutch Auction Factory")

    # Initialize test accounts
    master = sp.address("tz1-master-address-1234")
    owner = sp.address("tz1-owner-address-1234")

    # Instantiate Auction contract
    dutchAuction = DutchAuction()
    scenario += dutchAuction
