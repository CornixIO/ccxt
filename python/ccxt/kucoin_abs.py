# -*- coding: utf-8 -*-


class KucoinAbs:
    """Shared customizations for kucoin_spot and kucoin_futures."""

    def get_private_ws_details(self, params={}):
        response = self.privatePostBulletPrivate(params)
        data = self.safe_value(response, 'data', [])
        token = self.safe_string(data, 'token')
        servers = self.safe_value(data, 'instanceServers')
        if servers:
            server = servers[0]
            endpoint = self.safe_string(server, 'endpoint')
            ping_interval = self.safe_string(server, 'pingInterval')
            return {'token': token, 'endpoint': endpoint, 'ping_interval': ping_interval}
