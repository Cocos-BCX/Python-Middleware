import re
import sys
import threading
import websocket
import ssl
import json
import time
from itertools import cycle
# from grapheneapi.graphenewsrpc import GrapheneWebsocketRPC
from .exceptions import RPCError
from PythonMiddlewarebase.chains import known_chains
from . import exceptions
import logging
log = logging.getLogger(__name__)


class GrapheneWebsocketRPC(object):
    """ This class allows to call API methods synchronously, without
        callbacks. It logs in and registers to the APIs:

        * database
        * history

        :param str urls: Either a single Websocket URL, or a list of URLs
        :param str user: Username for Authentication
        :param str password: Password for Authentication
        :param Array apis: List of APIs to register to (default: ["database", "network_broadcast"])
        :param int num_retries: Try x times to num_retries to a node on disconnect, -1 for indefinitely

        Available APIs

              * database
              * network_node
              * network_broadcast
              * history

        Usage:

        .. code-block:: python

            ws = GrapheneWebsocketRPC("ws://10.0.0.16:8090","","")
            print(ws.get_account_count())

        .. note:: This class allows to call methods available via
                  websocket. If you want to use the notification
                  subsystem, please use ``GrapheneWebsocket`` instead.

    """
    def __init__(self, urls, user="", password="", **kwargs):
        self.api_id = {}
        self._request_id = 0
        if isinstance(urls, list):
            self.urls = cycle(urls)
        else:
            self.urls = cycle([urls])
        self.user = user
        self.password = password
        self.num_retries = kwargs.get("num_retries", -1)

        self.wsconnect()
        self.register_apis()

    def get_request_id(self):
        self._request_id += 1
        return self._request_id

    def wsconnect(self):
        cnt = 0
        while True:
            cnt += 1
            self.url = next(self.urls)
            log.debug("Trying to connect to node %s" % self.url)
            if self.url[:3] == "wss":
                sslopt_ca_certs = {'cert_reqs': ssl.CERT_NONE}
                self.ws = websocket.WebSocket(sslopt=sslopt_ca_certs)
            else:
                self.ws = websocket.WebSocket()
            try:
                self.ws.connect(self.url)
                break
            except KeyboardInterrupt:
                raise
            except:
                if (self.num_retries >= 0 and cnt > self.num_retries):
                    raise NumRetriesReached()

                sleeptime = (cnt - 1) * 2 if cnt < 10 else 10
                if sleeptime:
                    log.warning(
                        "Lost connection to node during wsconnect(): %s (%d/%d) "
                        % (self.url, cnt, self.num_retries) +
                        "Retrying in %d seconds" % sleeptime
                    )
                    time.sleep(sleeptime)
        self.login(self.user, self.password, api_id=1)

    def register_apis(self):
        self.api_id["database"] = self.database(api_id=1)
        self.api_id["history"] = self.history(api_id=1)
        self.api_id["network_broadcast"] = self.network_broadcast(api_id=1)

    """ RPC Calls
    """
    def rpcexec(self, payload):
        """ Execute a call by sending the payload

            :param json payload: Payload data
            :raises ValueError: if the server does not respond in proper JSON format
            :raises RPCError: if the server returns an error
        """
        log.debug(json.dumps(payload))
        cnt = 0
        while True:
            cnt += 1

            try:
                self.ws.send(json.dumps(payload, ensure_ascii=False).encode('utf8'))
                reply = self.ws.recv()
                break
            except KeyboardInterrupt:
                raise
            except:
                if (self.num_retries > -1 and
                        cnt > self.num_retries):
                    raise NumRetriesReached()
                sleeptime = (cnt - 1) * 2 if cnt < 10 else 10
                if sleeptime:
                    log.warning(
                        "Lost connection to node during rpcexec(): %s (%d/%d) "
                        % (self.url, cnt, self.num_retries) +
                        "Retrying in %d seconds" % sleeptime
                    )
                    time.sleep(sleeptime)

                # retry
                try:
                    self.ws.close()
                    time.sleep(sleeptime)
                    self.wsconnect()
                    self.register_apis()
                except:
                    pass

        ret = {}
        try:
            ret = json.loads(reply, strict=False)
        except ValueError:
            raise ValueError("Client returned invalid format. Expected JSON!")

        log.debug(json.dumps(reply))

        if 'error' in ret:
            if 'detail' in ret['error']:
                raise RPCError(ret['error']['detail'])
            else:
                raise RPCError(ret['error']['message'])
        else:
            return ret["result"]

    # End of Deprecated methods
    ####################################################################
    def __getattr__(self, name):
        """ Map all methods to RPC calls and pass through the arguments
        """
        def method(*args, **kwargs):

            # Sepcify the api to talk to
            if "api_id" not in kwargs:
                if ("api" in kwargs):
                    if (kwargs["api"] in self.api_id and
                            self.api_id[kwargs["api"]]):
                        api_id = self.api_id[kwargs["api"]]
                    else:
                        raise ValueError(
                            "Unknown API! "
                            "Verify that you have registered to %s"
                            % kwargs["api"]
                        )
                else:
                    api_id = 0
            else:
                api_id = kwargs["api_id"]

            # let's be able to define the num_retries per query
            self.num_retries = kwargs.get("num_retries", self.num_retries)

            query = {"method": "call",
                     "params": [api_id, name, list(args)],
                     "jsonrpc": "2.0",
                     "id": self.get_request_id()}
            r = self.rpcexec(query)
            return r
        return method


class NumRetriesReached(Exception):
    pass


class GrapheneNodeRPC(GrapheneWebsocketRPC):

    def __init__(self, *args, **kwargs):
        super(GrapheneNodeRPC, self).__init__(*args, **kwargs)
        chain_params=self.get_network()
        print("chain_params",chain_params)
        self.chain_params = chain_params

    def register_apis(self):
        self.api_id["database"] = self.database(api_id=1)
        self.api_id["history"] = self.history(api_id=1)
        self.api_id["network_broadcast"] = self.network_broadcast(api_id=1)

    def rpcexec(self, payload):
        """ Execute a call by sending the payload.
            It makes use of the GrapheneRPC library.
            In here, we mostly deal with Graphene specific error handling

            :param json payload: Payload data
            :raises ValueError: if the server does not respond in proper JSON format
            :raises RPCError: if the server returns an error
        """
        try:
            # print("payload>>>:", payload)
            # Forward call to GrapheneWebsocketRPC and catch+evaluate errors
            return super(GrapheneNodeRPC, self).rpcexec(payload)
        except exceptions.RPCError as e:
            msg = exceptions.decodeRPCErrorMsg(e).strip()
            if msg == "missing required active authority":
                raise exceptions.MissingRequiredActiveAuthority
            elif re.match("^no method with name.*", msg):
                raise exceptions.NoMethodWithName(msg)
            elif msg:
                raise exceptions.UnhandledRPCError(msg)
            else:
                raise e
        except Exception as e:
            raise e

    def get_account(self, name, **kwargs):
        """ Get full account details from account name or id

            :param str name: Account name or account id
        """
        if len(name.split(".")) == 3:
            return self.get_objects([name])[0]
        else:
            return self.get_account_by_name(name, **kwargs)

    def get_asset(self, name, **kwargs):
        """ Get full asset from name of id

            :param str name: Symbol name or asset id (e.g. 1.3.0)
        """
        if len(name.split(".")) == 3:
            return self.get_objects([name], **kwargs)[0]
        else:
            return self.lookup_asset_symbols([name], **kwargs)[0]

    def get_object(self, o, **kwargs):
        """ Get object with id ``o``

            :param str o: Full object id
        """
        return self.get_objects([o], **kwargs)[0]

    def get_network(self):
        """ Identify the connected network. This call returns a
            dictionary with keys chain_id, core_symbol and prefix
        """
        props = self.get_chain_properties()
        chain_id = props["chain_id"]
        for k, v in known_chains.items():
            if v["chain_id"] == chain_id:
                return v
        raise("Connecting to unknown network!")
