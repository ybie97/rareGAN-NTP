from .ntp_blackbox import NTPBlackbox


def create_blackbox_from_config(config):
    if config['blackbox'] == 'ntp':
        blackbox = NTPBlackbox(server_ip=config['ntp_server_ip'], num_process=config['num_process'])
        auxiliary = None
    else:
        raise ValueError('Unknown blackbox: {}'.format(config['blackbox']))

    return blackbox, auxiliary
