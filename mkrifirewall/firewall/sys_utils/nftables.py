from firewall.sys_utils.shell import run_command
from random import randint


class NFTablesException(Exception): pass


class NFTables:
    BACKUP_CONF_NAME = 'backup_conf.nft'
    NEW_CONF = 'new_conf.nft'

    DUMMY = {
        'tls1.1': randint(0, 1200),
        'ssl': randint(0, 100),
        'others': randint(0, 900),
        'ipsec': randint(0, 1500),
    }

    @classmethod
    def get_current_configuration(cls) -> str:
        conf, ret_code = run_command('nft list ruleset')
        if ret_code:
            raise NFTablesException("Error during configuration access")
        return conf

    @classmethod
    def _backup_conf(cls):
        run_command(f'nft list ruleset > {cls.BACKUP_CONF_NAME}')

    @classmethod
    def _restore_backup(cls):
        run_command(f'nft -f {cls.BACKUP_CONF_NAME}')

    @classmethod
    def _apply_conf(cls, conf):
        with open(cls.NEW_CONF, 'w') as f:
            f.write(conf)
        _, ret_code = run_command(f'nft -f {cls.NEW_CONF}')
        if ret_code:
            raise NFTablesException

    @classmethod
    def apply_current_conf(cls, conf: str):
        cls._backup_conf()
        try:
            cls._apply_conf(conf)
        except Exception as e:
            cls._restore_backup()
            raise e

    @classmethod
    def get_stats(cls):
        return cls.get_dummy_stats()

    @classmethod
    def get_dummy_stats(cls):
        for i, key in enumerate(cls.DUMMY.keys()):
            cls.DUMMY[key] += randint(0, 100 + i*20)
        return dict(cls.DUMMY)
