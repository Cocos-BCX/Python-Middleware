import PythonMiddleware as gph

_shared_graphene_instance = None

def shared_graphene_instance():
    """ This method will initialize ``_shared_graphene_instance`` and return it.
        The purpose of this method is to have offer single default
        graphene instance that can be reused by multiple classes.
    """
    global _shared_graphene_instance
    if not _shared_graphene_instance:
        _shared_graphene_instance = gph.Graphene()
    return _shared_graphene_instance
    #print("dasd")


def set_shared_graphene_instance(graphene_instance):
    """ This method allows us to override default graphene instance for all users of
        ``_shared_graphene_instance``.

        :param graphene.Graphene graphene_instance: Graphene instance
    """
    global _shared_graphene_instance
    _shared_graphene_instance = graphene_instance
