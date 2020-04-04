class NFTables:

    @classmethod
    def get_current_configuration(cls):
        return "{conf}"

    @classmethod
    def apply_current_cong(cls):
        raise NotImplementedError

    @classmethod
    def get_stats(cls):
        raise NotImplementedError
