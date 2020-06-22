asset_permissions = {}
asset_permissions["charge_market_fee"] = 0x01
asset_permissions["white_list"] = 0x02
asset_permissions["override_authority"] = 0x04
asset_permissions["transfer_restricted"] = 0x08
asset_permissions["disable_force_settle"] = 0x10
asset_permissions["global_settle"] = 0x20
asset_permissions["disable_issuer"] = 0x40
asset_permissions["witness_fed_asset"] = 0x80
asset_permissions["committee_fed_asset"] = 0x100


# enum asset_issuer_permission_flags
# {
# charge_market_fee = 0x01, /**< an issuer-specified percentage of all market trades in this asset is paid to the issuer */
# white_list = 0x02, /**< accounts must be whitelisted in order to hold this asset */
# override_authority = 0x04, /**< issuer may transfer asset back to himself */
# transfer_restricted = 0x08, /**< require the issuer to be one party to every transfer */
# disable_force_settle = 0x10, /**< disable force settling */
# global_settle = 0x20, /**< allow the bitasset issuer to force a global settling -- this may be set in permissions, but not flags */
# disable_issuer = 0x40, /**< allow the asset to be used with confidential transactions */
# witness_fed_asset = 0x80, /**< allow the asset to be fed by witnesses */
# committee_fed_asset = 0x100 /**< allow the asset to be fed by the committee */
# };


whitelist = {}
whitelist["no_listing"] = 0x0
whitelist["white_listed"] = 0x1
whitelist["black_listed"] = 0x2
whitelist["white_and_black_listed"] = 0x1 | 0x2

restricted = {}
restricted["all_restricted"] = 0
restricted["whitelist_authorities"] = 1
restricted["blacklist_authorities"] = 2
restricted["whitelist_markets"] = 3
restricted["blacklist_markets"] = 4


def toint(permissions):
    permissions_int = 0
    for p in permissions:
        if permissions[p]:
            permissions_int += asset_permissions[p]
    return permissions_int


def todict(number):
    r = {}
    for k, v in asset_permissions.items():
        r[k] = bool(number & v)
    return r


def force_flag(perms, flags):
    for p in flags:
        if flags[p]:
            perms |= asset_permissions[p]
    return perms


def test_permissions(perms, flags):
    for p in flags:
        if not asset_permissions[p] & perms:
            raise Exception(
                "Permissions prevent you from changing %s!" % p
            )
    return True
