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
            f.write(conf.replace('\r\n', '\n'))
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
        accepted = {}
        denied = {}

        for line in cls.get_current_configuration().splitlines():
            if "default" in line:
                line_array = line.split()
                if "accept" in line:
                    accepted["others"] = line_array[4]
                else:
                    denied["others"] = line_array[4]
            elif "packets" in line:
                line_array = line.split()
                key = line_array[2]
                if "accept" in line:
                    accepted[key] = line_array[7]
                else:
                    denied[key] = line_array[7]

        return cls._convert_str_to_int(accepted), cls._convert_str_to_int(denied)

    @staticmethod
    def _convert_str_to_int(data: dict):
        return {k: int(v) for k, v in data.items()}

    @classmethod
    def get_dummy_stats(cls):
        for i, key in enumerate(cls.DUMMY.keys()):
            cls.DUMMY[key] += randint(0, 100 + i * 20)
        return dict(cls.DUMMY)
