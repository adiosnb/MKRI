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
        """ Returns current nft configuration """
        conf, ret_code = run_command('nft list ruleset')
        if ret_code:
            raise NFTablesException("Error during configuration access")
        return conf

    @classmethod
    def _backup_conf(cls):
        """ Backups current nft configuration to a file """
        run_command(f'nft list ruleset > {cls.BACKUP_CONF_NAME}')

    @staticmethod
    def _delete_rules():
        """ Delete all rules from nft configuration """
        run_command('nft flush ruleset')

    @classmethod
    def _restore_backup(cls):
        """ Restores previous nft configuration from a file """
        run_command(f'nft -f {cls.BACKUP_CONF_NAME}')

    @classmethod
    def _apply_conf(cls, conf):
        """ Applies nft configuration submitted from webUI """
        with open(cls.NEW_CONF, 'w') as f:
            f.write(conf.replace('\r\n', '\n'))
        _, ret_code = run_command(f'nft -f {cls.NEW_CONF}')
        if ret_code:
            raise NFTablesException

    @classmethod
    def apply_current_conf(cls, conf: str):
        """ Handles application of submitted nft configuration """
        cls._backup_conf()
        cls._delete_rules()
        try:
            cls._apply_conf(conf)
        except Exception as e:
            cls._restore_backup()
            raise e

    @classmethod
    def get_stats(cls):
        """ Returns accepted and denied dictionaries containing statistics of current nft configuration """
        accepted = {}
        denied = {}

        for line in cls.get_current_configuration().splitlines():
            if "packets" in line:
                line_array = line.split()
                if line_array[0] == "counter":
                    if "accept" in line:
                        accepted["others"] = int(line_array[4])
                    else:
                        denied["others"] = int(line_array[4])
                    continue
                key = line_array[2]
                if key in accepted.keys():
                    accepted[key] += int(line_array[7])
                    continue
                elif key in denied.keys():
                    denied[key] += int(line_array[7])
                if "accept" in line:
                    accepted[key] = int(line_array[7])
                else:
                    denied[key] = int(line_array[7])

        return accepted, denied
