from wakeonlan import wake

def wake_server(mac_address: str) -> None:
    wake(mac_address)