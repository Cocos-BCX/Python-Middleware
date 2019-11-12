from .baseaccount import (
    PasswordKey as GPHPasswordKey,
    BrainKey as GPHBrainKey,
    Address as GPHAddress,
    PublicKey as GPHPublicKey,
    PrivateKey as GPHPrivateKey,
    re,hashlib,hexlify,os,BrainKeyDictionary
)
from .chains import default_prefix


class PasswordKey(GPHPasswordKey):
    """ This class derives a private key given the account name, the
        role and a password. It leverages the technology of Brainkeys
        and allows people to have a secure private key by providing a
        passphrase only.
    """

    def __init__(self, *args, **kwargs):
        super(PasswordKey, self).__init__(*args, **kwargs)


'''class BrainKey(GPHBrainKey):
    """Brainkey implementation similar to the graphene-ui web-wallet.

        :param str brainkey: Brain Key
        :param int sequence: Sequence number for consecutive keys

        Keys in Graphene are derived from a seed brain key which is a string of
        16 words out of a predefined dictionary with 49744 words. It is a
        simple single-chain key derivation scheme that is not compatible with
        BIP44 but easy to use.

        Given the brain key, a private key is derived as::

            privkey = SHA256(SHA512(brainkey + " " + sequence))

        Incrementing the sequence number yields a new key that can be
        regenerated given the brain key.
    """

    def __init__(self, *args, **kwargs):
        super(BrainKey, self).__init__(*args, **kwargs)
'''

class BrainKey(object):
    """Brainkey implementation similar to the graphene-ui web-wallet.

        :param str brainkey: Brain Key
        :param int sequence: Sequence number for consecutive keys

        Keys in Graphene are derived from a seed brain key which is a string of
        16 words out of a predefined dictionary with 49744 words. It is a
        simple single-chain key derivation scheme that is not compatible with
        BIP44 but easy to use.

        Given the brain key, a private key is derived as::

            privkey = SHA256(SHA512(brainkey + " " + sequence))

        Incrementing the sequence number yields a new key that can be
        regenerated given the brain key.

    """

    def __init__(self,prefix=default_prefix, brainkey=None, sequence=0):
        if not brainkey:
            self.brainkey = self.suggest()
        else:
            self.brainkey = self.normalize(brainkey).strip()
        self.sequence = sequence
        self.prefix = prefix

    def __next__(self):
        """ Get the next private key (sequence number increment) for
            iterators
        """
        return self.next_sequence()

    def next_sequence(self):
        """ Increment the sequence number by 1 """
        self.sequence += 1
        return self

    def normalize(self, brainkey):
        """ Correct formating with single whitespace syntax and no trailing space """
        return " ".join(re.compile("[\t\n\v\f\r ]+").split(brainkey))

    def get_brainkey(self):
        """ Return brain key of this instance """
        return self.normalize(self.brainkey)

    def get_private(self):
        """ Derive private key from the brain key and the current sequence
            number
        """
        encoded = "%s %d" % (self.brainkey, self.sequence)
        a = bytes(encoded, 'ascii')
        s = hashlib.sha256(hashlib.sha512(a).digest()).digest()
        return PrivateKey(hexlify(s).decode('ascii'),prefix=self.prefix)

    def get_public(self):
        return self.get_private().pubkey

    def get_private_key(self):
        return self.get_private()

    def get_public_key(self):
        return self.get_public()

    def suggest(self):
        """ Suggest a new random brain key. Randomness is provided by the
            operating system using ``os.urandom()``.
        """
        word_count = 16
        brainkey = [None] * word_count
        dict_lines = BrainKeyDictionary.split(',')
        assert len(dict_lines) == 49744
        for j in range(0, word_count):
            num = int.from_bytes(os.urandom(2), byteorder="little")
            rndMult = num / 2 ** 16  # returns float between 0..1 (inclusive)
            wIdx = round(len(dict_lines) * rndMult)
            brainkey[j] = dict_lines[wIdx]
        return " ".join(brainkey).upper()


class Address(GPHAddress):
    """ Address class

        This class serves as an address representation for Public Keys.

        :param str address: Base58 encoded address (defaults to ``None``)
        :param str pubkey: Base58 encoded pubkey (defaults to ``None``)
        :param str prefix: Network prefix (defaults to ``GPH``)

        Example::

           Address("GPHFN9r6VYzBK8EKtMewfNbfiGCr56pHDBFi")

    """
    def __init__(self, *args, **kwargs):
        if "prefix" not in kwargs:
            kwargs["prefix"] = default_prefix  # make prefix GPH
        super(Address, self).__init__(*args, **kwargs)


class PublicKey(GPHPublicKey):
    """ This class deals with Public Keys and inherits ``Address``.

        :param str pk: Base58 encoded public key
        :param str prefix: Network prefix (defaults to ``GPH``)

        Example:::

           PublicKey("GPH6UtYWWs3rkZGV8JA86qrgkG6tyFksgECefKE1MiH4HkLD8PFGL")

        .. note:: By default, graphene-based networks deal with **compressed**
                  public keys. If an **uncompressed** key is required, the
                  method ``unCompressed`` can be used::

                      PublicKey("xxxxx").unCompressed()

    """
    def __init__(self, *args, **kwargs):
        if "prefix" not in kwargs:
            kwargs["prefix"] = default_prefix  # make prefix GPH
        super(PublicKey, self).__init__(*args, **kwargs)


class PrivateKey(GPHPrivateKey):
    """ Derives the compressed and uncompressed public keys and
        constructs two instances of ``PublicKey``:

        :param str wif: Base58check-encoded wif key
        :param str prefix: Network prefix (defaults to ``GPH``)

        Example:::

            PrivateKey("5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd")

        Compressed vs. Uncompressed:

        * ``PrivateKey("w-i-f").pubkey``:
            Instance of ``PublicKey`` using compressed key.
        * ``PrivateKey("w-i-f").pubkey.address``:
            Instance of ``Address`` using compressed key.
        * ``PrivateKey("w-i-f").uncompressed``:
            Instance of ``PublicKey`` using uncompressed key.
        * ``PrivateKey("w-i-f").uncompressed.address``:
            Instance of ``Address`` using uncompressed key.

    """
    def __init__(self, *args, **kwargs):
        if "prefix" not in kwargs:
            kwargs["prefix"] = default_prefix  
        super(PrivateKey, self).__init__(*args, **kwargs)
